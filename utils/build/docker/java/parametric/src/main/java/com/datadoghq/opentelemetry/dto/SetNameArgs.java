package com.datadoghq.opentelemetry.dto;

import com.fasterxml.jackson.annotation.JsonProperty;

public record SetNameArgs(@JsonProperty("span_id") long spanId, String name) {
}
