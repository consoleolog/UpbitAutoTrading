package com.consoleolog.v1.model.dto;

import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

import java.util.List;

@Builder
@ToString
@Getter
public class EmaListDto {

    private List<Double> emaShortList;
    private List<Double> emaMidList;
    private List<Double> emaLongList;

    private EmaListDto(List<Double> emaShortList, List<Double> emaMidList, List<Double> emaLongList) {
        this.emaShortList = emaShortList;
        this.emaMidList = emaMidList;
        this.emaLongList = emaLongList;
    }


}
