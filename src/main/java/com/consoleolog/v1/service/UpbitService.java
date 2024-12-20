package com.consoleolog.v1.service;

import com.consoleolog.v1.model.dto.*;

import java.security.NoSuchAlgorithmException;
import java.util.List;

public interface UpbitService {

    List<CurrencyDto> getCurrencies();

    OrderResDto createOrder(OrderReqDto orderReqDto) throws NoSuchAlgorithmException;

    CurrencyDto getCurrency(String currency);

    List<CandleResDto> getCandles(CandleReqDto candleReqDto);


}
