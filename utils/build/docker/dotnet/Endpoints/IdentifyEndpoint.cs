using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Datadog.Trace;


namespace weblog
{
    public class IdentifyEndpoint : ISystemTestEndpoint
    {
        public void Register(Microsoft.AspNetCore.Routing.IEndpointRouteBuilder routeBuilder)
        {
            routeBuilder.MapGet("/identify", async context =>
            {

#if DDTRACE_HAS_USERDETAILS
                var userDetails = new UserDetails()
                {
                    Id = "usr.id",
                    Email = "usr.email",
                    Name = "usr.name",
                    SessionId = "usr.session_id",
                    Role = "usr.role",
                    Scope = "usr.scope",
                };
                var scope = Tracer.Instance.ActiveScope;
                scope?.Span.SetUser(userDetails);
#endif
 
                await context.Response.WriteAsync("Hello world!\\n");
            });

            routeBuilder.MapGet("/identify-propagate", async context =>
            {

#if DDTRACE_HAS_USERDETAILS
                var userDetails = new UserDetails()
                {
                    Id = "usr.id",
                    // TODO Needs new SDK version merging before enabling this next line
                    // PropagateId = true
                };
                var scope = Tracer.Instance.ActiveScope;
                scope?.Span.SetUser(userDetails);
#endif

                await context.Response.WriteAsync("Hello world!\\n");
            });
        }
    }
}
