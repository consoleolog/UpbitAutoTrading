package com.consoleolog.v1.model.dto.type;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonValue;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public enum OrderType {

    PRICE("price"),
    LIMIT("limit"),
    MARKET("market"),
    BEST("best");

    private final String value;

    @JsonValue
    public String getValue() {
        return value;
    }

    @JsonCreator
    public static OrderType fromValue(String value) {
        for (OrderType orderType : OrderType.values()) {
            if (orderType.getValue().equalsIgnoreCase(value)) {
                return orderType;
            }
        }
        throw new IllegalArgumentException("Unexpected value: " + value);
    }
}
