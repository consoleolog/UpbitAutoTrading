package com.consoleolog.v1.common.component;

import com.consoleolog.v1.model.dto.EmaListDto;
import com.consoleolog.v1.model.dto.MacdListDto;
import com.consoleolog.v1.model.dto.type.EmaType;


import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

@Slf4j
@RequiredArgsConstructor
@Component
public class StrategyComponent {

    public List<Double> createEmaList(EmaType emaType, List<Double> priceList){
        double day = (double) emaType.getValue();

        double k = 2 / ( 1 + (day -1) );

        double sma = 0;

        for (int i = 0; i < day; i++) {
            sma += priceList.get(i);
        }
        sma /= day;

        List<Double> emaList = new ArrayList<>();

        double ema = sma;
        for (int i = 0; i < priceList.size() - 1; i++) {
            ema = ( priceList.get(i) * k ) + ( ema * (1 - k) );
            emaList.add(ema);
        }
        return emaList;
    }

    public EmaListDto createEmaListDto(List<Double> priceList){

        List<Double> emaShortList = createEmaList(EmaType.SHORT,priceList);
        List<Double> emaMidList = createEmaList(EmaType.MID,priceList);
        List<Double> emaLongList = createEmaList(EmaType.LONG,priceList);

        return EmaListDto.builder()
                .emaMidList(emaMidList)
                .emaShortList(emaShortList)
                .emaLongList(emaLongList)
                .build();
    }

    public MacdListDto createMacdListDto(EmaListDto emaListDto){

        List<Double> macdUpList = new ArrayList<>();
        List<Double> macdMidList = new ArrayList<>();
        List<Double> macdLowList = new ArrayList<>();

        for (int i = 0; i < emaListDto.getEmaLongList().size(); i++) {
            double macdUp = emaListDto.getEmaShortList().get(i) - emaListDto.getEmaMidList().get(i);
            macdUpList.add(macdUp);
            double macdMid = emaListDto.getEmaShortList().get(i) - emaListDto.getEmaLongList().get(i);
            macdMidList.add(macdMid);
            double macdLow = emaListDto.getEmaMidList().get(i) - emaListDto.getEmaLongList().get(i);
            macdLowList.add(macdLow);
        }

        return MacdListDto.builder()
                .macdUpList(macdUpList)
                .macdMidList(macdMidList)
                .macdLowList(macdLowList)
                .build();
    }





}
