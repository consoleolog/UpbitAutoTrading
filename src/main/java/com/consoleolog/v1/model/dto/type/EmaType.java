package com.consoleolog.v1.model.dto.type;

import lombok.AllArgsConstructor;
import lombok.Getter;

@AllArgsConstructor
@Getter
public enum EmaType {

    SHORT(10),
    MID(20),
    LONG(40);

    private final Integer value;
}
