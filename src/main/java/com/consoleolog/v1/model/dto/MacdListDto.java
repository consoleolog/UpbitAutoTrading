package com.consoleolog.v1.model.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

import java.util.List;

@Builder
@ToString
@Getter
public class MacdListDto {

    private List<Double> macdUpList;
    private List<Double> macdMidList;
    private List<Double> macdLowList;

    private MacdListDto(List<Double> macdUpList, List<Double> macdMidList, List<Double> macdLowList ) {
        this.macdUpList = macdUpList;
        this.macdMidList = macdMidList;
        this.macdLowList = macdLowList;
    }

}
