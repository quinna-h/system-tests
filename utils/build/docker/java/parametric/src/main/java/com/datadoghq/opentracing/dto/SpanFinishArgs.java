package com.datadoghq.opentracing.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record SpanFinishArgs(@JsonProperty("span_id") long spanId) {
}