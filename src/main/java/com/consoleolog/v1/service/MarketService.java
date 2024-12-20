package com.consoleolog.v1.service;

import com.consoleolog.v1.model.dto.CandleResDto;
import com.consoleolog.v1.model.dto.EmaListDto;
import com.consoleolog.v1.model.dto.MacdListDto;

import com.consoleolog.v1.model.entity.Market;

public interface MarketService {

    Market saveData(CandleResDto candleResDto, EmaListDto emaListDto, MacdListDto macdListDto, String interval);
}
