package com.consoleolog.global.config;

import com.consoleolog.v1.common.component.StrategyComponent;
import com.consoleolog.v1.common.util.CommonUtils;
import com.consoleolog.v1.model.dto.*;
import com.consoleolog.v1.model.dto.type.IntervalType;
import com.consoleolog.v1.model.dto.type.OrderType;
import com.consoleolog.v1.model.dto.type.SideType;
import com.consoleolog.v1.service.MarketService;
import com.consoleolog.v1.common.component.UpbitComponent;
import com.consoleolog.v1.service.OrderService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.batch.core.JobExecutionException;

import org.springframework.context.annotation.Configuration;
import org.springframework.scheduling.annotation.Scheduled;

import java.security.NoSuchAlgorithmException;
import java.util.List;

@Slf4j
@RequiredArgsConstructor
@Configuration
public class ScheduleConfig {

    private final UpbitComponent upbitComponent;

    private final StrategyComponent strategyComponent;

    private final MarketService marketService;

    private final OrderService orderService;

    @Scheduled(cron = "0 0/1 * * * ?", zone = "Asia/Seoul")
    public void getMinutes1() throws JobExecutionException {

    }

    @Scheduled(cron = "0 0/3 * * * ?", zone = "Asia/Seoul")
    public void getMinutes3() throws JobExecutionException, NoSuchAlgorithmException {

        IntervalType intervalType = IntervalType.MINUTE;

        int unit = 3;

        CandleReqDto candleReqDto = CandleReqDto.builder()
                .market("KRW-BTC")
                .interval(intervalType)
                .unit(unit)
                .build();

        String interval = intervalType + String.valueOf(unit);

        List<CandleResDto> candleResDtoList = upbitComponent.getCandles(candleReqDto);

        List<Double> prices = candleResDtoList.stream().map(CandleResDto::getTradePrice).toList();

        EmaListDto emaListDto = strategyComponent.createEmaListDto(prices);

        MacdListDto macdListDto = strategyComponent.createMacdListDto(emaListDto);

        marketService.saveData(candleResDtoList.get(0), emaListDto, macdListDto, interval);

        boolean decisionBuy = decisionBuy(emaListDto, macdListDto);

        boolean decisionSell = decisionSell(emaListDto, macdListDto);

        if (decisionBuy) {
            OrderReqDto orderReqDto = OrderReqDto.builder()
                    .market("KRW-BTC")
                    .side(SideType.BUY)
                    .orderType(OrderType.PRICE)
                    .price(6000d)
                    .identifier(CommonUtils.createRandomDateString())
                    .build();

            orderService.executeOrder(orderReqDto);
        }

        if (decisionSell) {
            OrderReqDto orderReqDto = OrderReqDto.builder()
                    .market("KRW-BTC")
                    .side(SideType.SELL)
                    .orderType(OrderType.MARKET)
                    .volume(upbitComponent.getCurrency("KRW-BTC").getBalance())
                    .identifier(CommonUtils.createRandomDateString())
                    .build();
            orderService.executeOrder(orderReqDto);
        }
    }

    private double getSlopeByCurrent(List<Double> aList, Integer num){
        return aList.get(0) - aList.get(1 + num) / num;
    }


    private boolean decisionBuy(EmaListDto emaListDto, MacdListDto macdListDto){

        int stage = CommonUtils.getStage(emaListDto);

        double macdUpSlope1 = getSlopeByCurrent(macdListDto.getMacdUpList(), 1);

        double macdMidSlope1 = getSlopeByCurrent(macdListDto.getMacdMidList(), 1);

        double macdLowSlope1 = getSlopeByCurrent(macdListDto.getMacdLowList(), 1);

        if ((stage == 4 || stage == 5 ) && macdUpSlope1 > 0 && macdMidSlope1 > 0 && macdLowSlope1 > 0){
            double macdUpSlope2 = getSlopeByCurrent(macdListDto.getMacdUpList(), 2);
            double macdMidSlope2 = getSlopeByCurrent(macdListDto.getMacdMidList(), 2);
            double macdLowSlope2 = getSlopeByCurrent(macdListDto.getMacdLowList(), 2);

            if (macdUpSlope2 > 0 && macdMidSlope2 > 0 && macdLowSlope2 > 0){
                double macdUpSlope3 = getSlopeByCurrent(macdListDto.getMacdUpList(), 3);
                double macdMidSlope3 = getSlopeByCurrent(macdListDto.getMacdMidList(), 3);
                double macdLowSlope3 = getSlopeByCurrent(macdListDto.getMacdLowList(), 3);

                if (macdUpSlope3 > 0 && macdMidSlope3 > 0 && macdLowSlope3 > 0){
                    double macdUpSlope4 = getSlopeByCurrent(macdListDto.getMacdUpList(), 4);
                    double macdMidSlope4 = getSlopeByCurrent(macdListDto.getMacdMidList(), 4);

                    if (macdUpSlope4 > 0 && macdMidSlope4 > 0){
                        double macdUpSlope5 = getSlopeByCurrent(macdListDto.getMacdUpList(), 5);
                        if (macdUpSlope5 > 0)
                            return true;
                    }

                }
            }
        }
        return false;
    }

    private boolean decisionSell(EmaListDto emaListDto, MacdListDto macdListDto){

        int stage = CommonUtils.getStage(emaListDto);

        double macdUpSlope1 = getSlopeByCurrent(macdListDto.getMacdUpList(), 1);

        double macdMidSlope1 = getSlopeByCurrent(macdListDto.getMacdMidList(), 1);

        double macdLowSlope1 = getSlopeByCurrent(macdListDto.getMacdLowList(), 1);

        if ((stage == 1 || stage == 2 ) && macdUpSlope1 < 0 && macdMidSlope1 < 0 && macdLowSlope1 < 0){
            double macdUpSlope2 = getSlopeByCurrent(macdListDto.getMacdUpList(), 2);
            double macdMidSlope2 = getSlopeByCurrent(macdListDto.getMacdMidList(), 2);
            double macdLowSlope2 = getSlopeByCurrent(macdListDto.getMacdLowList(), 2);

            if (macdUpSlope2 < 0 && macdMidSlope2 < 0 && macdLowSlope2 < 0){
                double macdUpSlope3 = getSlopeByCurrent(macdListDto.getMacdUpList(), 3);
                double macdMidSlope3 = getSlopeByCurrent(macdListDto.getMacdMidList(), 3);
                double macdLowSlope3 = getSlopeByCurrent(macdListDto.getMacdLowList(), 3);

                if (macdUpSlope3 < 0 && macdMidSlope3 < 0 && macdLowSlope3 < 0){
                    double macdUpSlope4 = getSlopeByCurrent(macdListDto.getMacdUpList(), 4);
                    double macdMidSlope4 = getSlopeByCurrent(macdListDto.getMacdMidList(), 4);

                    if (macdUpSlope4 < 0 && macdMidSlope4 < 0){
                        double macdUpSlope5 = getSlopeByCurrent(macdListDto.getMacdUpList(), 5);
                        if (macdUpSlope5 < 0)
                            return true;
                    }
                }
            }
        }
        return false;
    }




}
