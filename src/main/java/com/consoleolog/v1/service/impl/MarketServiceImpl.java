package com.consoleolog.v1.service.impl;

import com.consoleolog.v1.common.util.CommonUtils;
import com.consoleolog.v1.common.component.StrategyComponent;
import com.consoleolog.v1.model.dto.CandleResDto;
import com.consoleolog.v1.model.dto.EmaListDto;
import com.consoleolog.v1.model.dto.MacdListDto;
import com.consoleolog.v1.model.dto.type.IntervalType;
import com.consoleolog.v1.model.entity.Market;
import com.consoleolog.v1.repository.MarketRepository;
import com.consoleolog.v1.service.MarketService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@RequiredArgsConstructor
@Service
public class MarketServiceImpl implements MarketService {

    private final StrategyComponent strategyComponent;

    private final MarketRepository marketRepository;

    public Market saveData(CandleResDto candleResDto, EmaListDto emaListDto, MacdListDto macdListDto, String interval){

        Integer stage = CommonUtils.getStage(emaListDto);

        Market market = Market
                .builder()
                .ticker(candleResDto.getMarket())
                .interval(interval)
                .price(candleResDto.getTradePrice())
                .emaShort(emaListDto.getEmaShortList().get(0))
                .emaMid(emaListDto.getEmaMidList().get(0))
                .emaLong(emaListDto.getEmaLongList().get(0))
                .stage(stage)
                .macdUp(macdListDto.getMacdUpList().get(0))
                .macdMid(macdListDto.getMacdMidList().get(0))
                .macdLow(macdListDto.getMacdLowList().get(0))
                .build();

        return marketRepository.save(market);
    }

}
