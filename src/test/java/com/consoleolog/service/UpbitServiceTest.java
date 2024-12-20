package com.consoleolog.service;

import com.consoleolog.v1.model.dto.*;
import com.consoleolog.v1.model.dto.type.IntervalType;
import com.consoleolog.v1.model.dto.type.OrderType;
import com.consoleolog.v1.model.dto.type.SideType;
import com.consoleolog.v1.common.component.UpbitComponent;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.security.NoSuchAlgorithmException;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;

@SpringBootTest
public class UpbitServiceTest {

    private final UpbitComponent upbitService;

    @Autowired
    public UpbitServiceTest(
            UpbitComponent upbitService
    ) {
        this.upbitService = upbitService;
    }

    @Test
    public void testCreateOrderForBuy() throws NoSuchAlgorithmException {
        OrderReqDto orderReqDto = OrderReqDto.builder()
                .market("KRW-BTC")
                .side(SideType.BUY)
                .price(6000d)
                .orderType(OrderType.PRICE)
                .build();

        OrderResDto orderResDto = upbitService.createOrder(orderReqDto);

        System.out.println(orderResDto);
    }

    @Test
    public void testCreateOrderForSell() throws NoSuchAlgorithmException {
        CurrencyDto currencyDto = upbitService.getCurrency("BTC");

        OrderReqDto orderReqDto = OrderReqDto.builder()
                .market("KRW-BTC")
                .side(SideType.SELL)
                .volume(currencyDto.getBalance())
                .orderType(OrderType.MARKET)
                .build();

        OrderResDto orderResDto = upbitService.createOrder(orderReqDto);
        System.out.println(orderResDto);

    }

    @Test
    public void testStrategy(){
        CandleReqDto candleReqDto = CandleReqDto
                .builder()
                .market("KRW-BTC")
                .interval(IntervalType.DAY)
                .count(3)
                .build();

        List<CandleResDto> candleResList = upbitService.getCandles(candleReqDto);

        System.out.println(candleResList.get(0));
        System.out.println(candleResList.get(1));
        System.out.println(candleResList.get(2));

        candleResList = candleResList.stream()
                .sorted(Comparator.comparing(CandleResDto::getTimestamp))
                .toList();

        System.out.println(candleResList.get(0));
        System.out.println(candleResList.get(1));
        System.out.println(candleResList.get(2));

        double zero = 0;

        List<Double> upList = new ArrayList<>();
        List<Double> downList = new ArrayList<>();

        for (int i = 0; i < candleResList.size() - 1; i++) {
            /* 최근 종가 - 전일 종가 = gap 값이 양수면 상승 / 음수면 하락 */
            double gapByTradePrice = candleResList.get(i + 1).getTradePrice() - candleResList.get(i).getTradePrice();

            if (gapByTradePrice > 0){
                upList.add(gapByTradePrice);
                downList.add(zero);
            } else if (gapByTradePrice < 0){
                downList.add(gapByTradePrice);
                upList.add(zero);
            } else {
                upList.add(zero);
                downList.add(zero);
            }
        }







        double day = 14;
        double a = (double) 1 / (1 + (day - 1));

        System.out.println(upList);
        System.out.println(downList);


    }



    @Test
    public void testCalMacd(){




    }



}
