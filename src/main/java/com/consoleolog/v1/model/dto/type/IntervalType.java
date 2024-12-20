package com.consoleolog.v1.model.dto.type;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum IntervalType {

    SECOND("seconds"),
    MINUTE("minutes"),
    DAY("days"),
    WEEK("weeks"),
    MONTH("months"),
    YEAR("years");

    private final String value;

}
