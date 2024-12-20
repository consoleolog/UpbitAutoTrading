package com.consoleolog.v1.model.dto;

import com.consoleolog.v1.model.dto.type.IntervalType;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Builder
@ToString
@Getter
public class CandleReqDto {

    private IntervalType interval;

    private String market;

    private String to;

    @Builder.Default
    private Integer count = 200;

    private Integer unit;

    private CandleReqDto(IntervalType interval, String market, String to, Integer count, Integer unit) {
        this.interval = interval;
        this.market = market;
        this.to = to;
        this.count = count;
        this.unit = unit;
    }
}
