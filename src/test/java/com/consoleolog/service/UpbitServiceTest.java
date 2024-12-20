package com.consoleolog.service;

import com.consoleolog.v1.model.dto.CurrencyDto;
import com.consoleolog.v1.model.dto.OrderReqDto;
import com.consoleolog.v1.model.dto.OrderResDto;
import com.consoleolog.v1.model.dto.type.OrderType;
import com.consoleolog.v1.model.dto.type.SideType;
import com.consoleolog.v1.service.UpbitService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.security.NoSuchAlgorithmException;

@SpringBootTest
public class UpbitServiceTest {

    private final UpbitService upbitService;

    @Autowired
    public UpbitServiceTest(
            UpbitService upbitService
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

}
