using Datadog.Trace;
using System.Reflection;
using System.Threading;
using Newtonsoft.Json;

namespace ApmTestApi.Endpoints;

public abstract class ApmTestApi
{
    public static void MapApmTraceEndpoints(WebApplication app, ILogger<ApmTestApi> logger)
    {
        _logger = logger;
        // TODO: Remove when the Tracer sets the correct results in the SpanContextPropagator.Instance getter
        // This should avoid a bug in the SpanContextPropagator.Instance getter where it is populated WITHOUT consulting the TracerSettings.
        // By instantiating the Tracer first, that faulty getter code path will not be invoked
        _ = Tracer.Instance;

        app.MapGet("/trace/crash", Crash);
        app.MapGet("/trace/config", GetTracerConfig);
        app.MapPost("/trace/tracer/stop", StopTracer);
        app.MapPost("/trace/span/start", StartSpan);
        app.MapPost("/trace/span/inject_headers", InjectHeaders);
        app.MapPost("/trace/span/extract_headers", ExtractHeaders);

        app.MapPost("/trace/span/error", SpanSetError);
        app.MapPost("/trace/span/set_meta", SpanSetMeta);
        app.MapPost("/trace/span/set_metric", SpanSetMetric);
        app.MapPost("/trace/span/finish", FinishSpan);
        app.MapPost("/trace/span/flush", FlushSpans);
    }

    // Core types
    private static readonly Type SpanType = Type.GetType("Datadog.Trace.Span, Datadog.Trace", throwOnError: true)!;
    private static readonly Type SpanContextType = Type.GetType("Datadog.Trace.SpanContext, Datadog.Trace", throwOnError: true)!;
    private static readonly Type TracerType = Type.GetType("Datadog.Trace.Tracer, Datadog.Trace", throwOnError: true)!;
    private static readonly Type TracerManagerType = Type.GetType("Datadog.Trace.TracerManager, Datadog.Trace", throwOnError: true)!;
    private static readonly Type GlobalSettingsType = Type.GetType("Datadog.Trace.Configuration.GlobalSettings, Datadog.Trace", throwOnError: true)!;
    private static readonly Type ImmutableTracerSettingsType = Type.GetType("Datadog.Trace.Configuration.ImmutableTracerSettings, Datadog.Trace", throwOnError: true)!;

    // Propagator types
    internal static readonly Type W3CTraceContextPropagatorType = Type.GetType("Datadog.Trace.Propagators.W3CTraceContextPropagator, Datadog.Trace", throwOnError: true)!;

    // Agent-related types
    private static readonly Type AgentWriterType = Type.GetType("Datadog.Trace.Agent.AgentWriter, Datadog.Trace", throwOnError: true)!;
    internal static readonly Type StatsAggregatorType = Type.GetType("Datadog.Trace.Agent.StatsAggregator, Datadog.Trace", throwOnError: true)!;

    // Accessors for internal properties/fields accessors
    internal static readonly PropertyInfo GetGlobalSettingsInstance  = GlobalSettingsType.GetProperty("Instance", BindingFlags.Static | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo GetTracerManager = TracerType.GetProperty("TracerManager", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly MethodInfo GetAgentWriter = TracerManagerType.GetProperty("AgentWriter", BindingFlags.Instance | BindingFlags.Public)!.GetGetMethod()!;
    internal static readonly FieldInfo GetStatsAggregator = AgentWriterType.GetField("_statsAggregator", BindingFlags.Instance | BindingFlags.NonPublic)!;
    private static readonly PropertyInfo SpanContext = SpanType.GetProperty("Context", BindingFlags.Instance | BindingFlags.NonPublic)!;
    private static readonly PropertyInfo Origin = SpanContextType.GetProperty("Origin", BindingFlags.Instance | BindingFlags.NonPublic)!;

    internal static readonly PropertyInfo SamplingPriority = SpanContextType.GetProperty("SamplingPriority", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo RawTraceId = SpanContextType.GetProperty("RawTraceId", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo RawSpanId = SpanContextType.GetProperty("RawSpanId", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo AdditionalW3CTraceState = SpanContextType.GetProperty("AdditionalW3CTraceState", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo PropagationStyleInject = ImmutableTracerSettingsType.GetProperty("PropagationStyleInject", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo RuntimeMetricsEnabled = ImmutableTracerSettingsType.GetProperty("RuntimeMetricsEnabled", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo IsActivityListenerEnabled = ImmutableTracerSettingsType.GetProperty("IsActivityListenerEnabled", BindingFlags.Instance | BindingFlags.NonPublic)!;
    internal static readonly PropertyInfo GetTracerInstance = TracerType.GetProperty("Instance", BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public)!;
    internal static readonly PropertyInfo GetTracerSettings = TracerType.GetProperty("Settings", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public)!;
    internal static readonly PropertyInfo GetDebugEnabled = GlobalSettingsType.GetProperty("DebugEnabled", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public)!;

    // Propagator methods
    internal static readonly MethodInfo W3CTraceContextCreateTraceStateHeader = W3CTraceContextPropagatorType.GetMethod("CreateTraceStateHeader", BindingFlags.Static | BindingFlags.NonPublic)!;

    // StatsAggregator flush methods
    private static readonly MethodInfo StatsAggregatorDisposeAsync = StatsAggregatorType.GetMethod("DisposeAsync", BindingFlags.Instance | BindingFlags.Public)!;
    private static readonly MethodInfo StatsAggregatorFlush = StatsAggregatorType.GetMethod("Flush", BindingFlags.Instance | BindingFlags.NonPublic)!;

    private static readonly Dictionary<ulong, ISpan> Spans = new();
    private static readonly Dictionary<ulong, Datadog.Trace.ISpanContext> DDContexts = new();

    internal static ILogger<ApmTestApi>? _logger;

    internal static readonly SpanContextInjector _spanContextInjector = new();
    internal static readonly SpanContextExtractor _spanContextExtractor = new();

    internal static IEnumerable<string> GetHeaderValues(string[][] headersList, string key)
    {
        List<string> values = new List<string>();
        foreach (var kvp in headersList)
        {
            if (kvp.Length == 2 && string.Equals(key, kvp[0], StringComparison.OrdinalIgnoreCase))
            {
                values.Add(kvp[1]);
            }
        }

        return values.AsReadOnly();
    }

    public static async Task StopTracer()
    {
        await Tracer.Instance.ForceFlushAsync();
    }

    private static async Task<string> StartSpan(HttpRequest request)
    {
        var headerRequestBody = await new StreamReader(request.Body).ReadToEndAsync();
        var parsedDictionary = JsonConvert.DeserializeObject<Dictionary<string, Object>>(headerRequestBody);

        _logger?.LogInformation("StartSpan: {HeaderRequestBody}", headerRequestBody);

        var creationSettings = new SpanCreationSettings
        {
            FinishOnClose = false,
        };

        if (parsedDictionary!.TryGetValue("parent_id", out var parentId) && parentId is not null)
        {
            var longParentId = Convert.ToUInt64(parentId);
            if(Spans.TryGetValue(longParentId, out var parentSpan)) {
                creationSettings.Parent = parentSpan.Context;
            } else if (DDContexts.TryGetValue(longParentId, out var ddContext)) {
                creationSettings.Parent = ddContext;
            } else {
                throw new Exception($"Parent span with id {longParentId} not found");
            }
        }

        parsedDictionary.TryGetValue("name", out var name);
        using var scope = Tracer.Instance.StartActive(operationName: name!.ToString()!, creationSettings);
        var span = scope.Span;

        if (parsedDictionary.TryGetValue("service", out var service) && service is not null)
        {
            span.ServiceName = service.ToString();
        }

        if (parsedDictionary.TryGetValue("resource", out var resource) && resource is not null)
        {
            span.ResourceName = resource.ToString();
        }

        if (parsedDictionary.TryGetValue("type", out var type)  && type is not null)
        {
            span.Type = type.ToString();
        }

        if (parsedDictionary.TryGetValue("span_tags", out var tagsToken))
        {
            foreach (var tag in (Newtonsoft.Json.Linq.JArray)tagsToken)
            {
                var key = (string)tag[0]!;
                var value = (string?)tag[1];

                span.SetTag(key, value);
            }
        }

        Spans[span.SpanId] = span;

        return JsonConvert.SerializeObject(new
        {
            span_id = span.SpanId.ToString(),
            trace_id = span.TraceId.ToString(),
        });
    }

    private static async Task SpanSetMeta(HttpRequest request)
    {
        var headerBodyDictionary = await new StreamReader(request.Body).ReadToEndAsync();
        var parsedDictionary = JsonConvert.DeserializeObject<Dictionary<string, string>>(headerBodyDictionary);
        parsedDictionary!.TryGetValue("span_id", out var id);
        parsedDictionary.TryGetValue("key", out var key);
        parsedDictionary.TryGetValue("value", out var value);

        var span = Spans[Convert.ToUInt64(id)];
        span.SetTag(key!, value);
    }

    private static async Task SpanSetMetric(HttpRequest request)
    {
        var headerBodyDictionary = await new StreamReader(request.Body).ReadToEndAsync();
        var parsedDictionary = JsonConvert.DeserializeObject<Dictionary<string, string>>(headerBodyDictionary)!;
        parsedDictionary.TryGetValue("span_id", out var id);
        parsedDictionary.TryGetValue("key", out var key);
        parsedDictionary.TryGetValue("value", out var value);

        var span = Spans[Convert.ToUInt64(id)];
        span.SetTag(key!, Convert.ToDouble(value));
    }

    private static async Task SpanSetError(HttpRequest request)
    {
        var span = Spans[Convert.ToUInt64(await FindBodyKeyValueAsync(request, "span_id"))];
        span.Error = true;

        var type = await FindBodyKeyValueAsync(request, "type");
        var message = await FindBodyKeyValueAsync(request, "message");
        var stack = await FindBodyKeyValueAsync(request, "stack");

        if (!string.IsNullOrEmpty(type))
        {
            span.SetTag(Tags.ErrorType, type);
        }

        if (!string.IsNullOrEmpty(message))
        {
            span.SetTag(Tags.ErrorMsg, message);
        }

        if (!string.IsNullOrEmpty(stack))
        {
            span.SetTag(Tags.ErrorStack, stack);
        }
    }

    private static async Task<string> ExtractHeaders(HttpRequest request)
    {
        var headerRequestBody = await new StreamReader(request.Body).ReadToEndAsync();
        var parsedDictionary = JsonConvert.DeserializeObject<Dictionary<string, Object>>(headerRequestBody);
        var headersList = (Newtonsoft.Json.Linq.JArray)parsedDictionary!["http_headers"];
        var extractedContext = _spanContextExtractor.Extract(
            headersList.ToObject<string[][]>()!,
            getter: GetHeaderValues
        );

        String extractedSpanId = null;
        if (extractedContext is not null)
        {
            DDContexts[extractedContext.SpanId] = extractedContext;
            extractedSpanId = extractedContext.SpanId.ToString();
        }

        return JsonConvert.SerializeObject(new
        {
            span_id = extractedSpanId
        });
    }

    private static async Task<string> InjectHeaders(HttpRequest request)
    {
        var httpHeaders = new List<string[]>();

        var spanId = await FindBodyKeyValueAsync(request, "span_id");

        if (!string.IsNullOrEmpty(spanId as string) && Spans.TryGetValue(Convert.ToUInt64(spanId), out var span))
        {
            // Define a function to set headers in HttpRequestHeaders
            static void Setter(List<string[]> headers, string key, string value) =>
                headers.Add(new string[] { key, value });

            Console.WriteLine(JsonConvert.SerializeObject(new
            {
                HttpHeaders = httpHeaders
            }));

            // Invoke SpanContextPropagator.Inject with the HttpRequestHeaders
            _spanContextInjector.Inject(httpHeaders, Setter, span.Context);
        }

        return JsonConvert.SerializeObject(new
        {
            http_headers = httpHeaders
        });
    }

    private static async Task FinishSpan(HttpRequest request)
    {
        var span = Spans[Convert.ToUInt64(await FindBodyKeyValueAsync(request, "span_id"))];
        span.Finish();
    }

    private static string Crash(HttpRequest request)
    {
        var thread = new Thread(() =>
        {
            throw new BadImageFormatException("Expected");
        });

        thread.Start();
        thread.Join();

        return "Failed to crash";
    }

    private static string GetTracerConfig(HttpRequest request)
    {
        var tracerSettings = Tracer.Instance.Settings;
        var internalTracer = GetTracerInstance.GetValue(null);
        var internalTracerSettings = GetTracerSettings.GetValue(internalTracer);

        var globalSettings = GetGlobalSettingsInstance.GetValue(null)!;
        var debugEnabled = (bool)GetDebugEnabled.GetValue(globalSettings)!;

        var propagationStyleInject = (string[])PropagationStyleInject.GetValue(internalTracerSettings)!;
        var runtimeMetricsEnabled = (bool)RuntimeMetricsEnabled.GetValue(internalTracerSettings)!;
        var isOtelEnabled = (bool)IsActivityListenerEnabled.GetValue(internalTracerSettings)!;

        Dictionary<string, object?> config = new()
        {
            { "dd_service", tracerSettings.ServiceName },
            { "dd_env", tracerSettings.Environment },
            { "dd_version", tracerSettings.ServiceVersion },
            { "dd_trace_sample_rate", tracerSettings.GlobalSamplingRate },
            { "dd_trace_enabled", tracerSettings.TraceEnabled.ToString().ToLowerInvariant() },
            { "dd_runtime_metrics_enabled", runtimeMetricsEnabled.ToString().ToLowerInvariant() },
            { "dd_tags", tracerSettings.GlobalTags.Select(kvp => $"{kvp.Key}:{kvp.Value}").ToArray() },
            { "dd_trace_propagation_style", string.Join(",", propagationStyleInject) },
            { "dd_trace_debug", debugEnabled ? "true" : "false" },
            { "dd_trace_otel_enabled", isOtelEnabled.ToString().ToLowerInvariant() },
            { "dd_log_level", null },
            { "dd_trace_agent_url", tracerSettings.AgentUri },
            { "dd_trace_rate_limit", tracerSettings.MaxTracesSubmittedPerSecond.ToString() },
            // { "dd_trace_sample_ignore_parent", "null" }, // Not supported
        };

        return JsonConvert.SerializeObject(new
        {
            config = config
        });
    }

    internal static async Task FlushSpans()
    {
        if (Tracer.Instance is null)
        {
            throw new NullReferenceException("Tracer.Instance is null");
        }

        await Tracer.Instance.ForceFlushAsync();
        Spans.Clear();
        ApmTestApiOtel.Activities.Clear();
    }

    internal static async Task FlushTraceStats()
    {
        if (GetTracerManager is null)
        {
            throw new NullReferenceException("GetTracerManager is null");
        }

        if (Tracer.Instance is null)
        {
            throw new NullReferenceException("Tracer.Instance is null");
        }

        var tracerManager = GetTracerManager.GetValue(GetTracerInstance.GetValue(null));
        var agentWriter = GetAgentWriter.Invoke(tracerManager, null);
        var statsAggregator = GetStatsAggregator.GetValue(agentWriter);

        if (statsAggregator?.GetType() == StatsAggregatorType)
        {
            var disposeAsyncTask = StatsAggregatorDisposeAsync.Invoke(statsAggregator, null) as Task;
            await disposeAsyncTask!;


            // Invoke StatsAggregator.Flush()
            // If StatsAggregator.DisposeAsync() was previously called during the lifetime of the application,
            // then no stats will be flushed when StatsAggregator.DisposeAsync() returns.
            // To be safe, perform an extra flush to ensure that we have flushed the stats
            var flushTask = StatsAggregatorFlush.Invoke(statsAggregator, null) as Task;
            await flushTask!;
        }
    }

    internal static async Task<string> FindBodyKeyValueAsync(HttpRequest httpRequest, string keyToFind)
    {
        var headerBodyDictionary = await new StreamReader(httpRequest.Body).ReadToEndAsync();
        var parsedDictionary = JsonConvert.DeserializeObject<Dictionary<string, string>>(headerBodyDictionary);
        var keyFound = parsedDictionary!.TryGetValue(keyToFind, out var foundValue);

        return keyFound ? foundValue! : String.Empty;
    }
}
