package com.consoleolog.v1.model.dto.type;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public enum SideType {

    BUY("bid"),
    SELL("ask");

    private final String value;

    @JsonValue
    public String getValue() {
        return value;
    }

    @JsonCreator
    public static SideType fromValue(String value) {
        for (SideType side : SideType.values()) {
            if (side.getValue().equals(value)) {
                return side;
            }
        }
        throw new IllegalArgumentException("Unexpected value: " + value);
    }
}
