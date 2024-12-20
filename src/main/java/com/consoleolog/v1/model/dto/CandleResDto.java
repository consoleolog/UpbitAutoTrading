package com.consoleolog.v1.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.ToString;

import java.time.Instant;
import java.time.LocalDateTime;
import java.time.ZoneId;

@ToString
@Getter
public class CandleResDto {

    @JsonProperty("market")
    private String market;

    @JsonProperty("candle_date_time_utc")
    private LocalDateTime candleDateTimeUtc;

    @JsonProperty("candle_date_time_kst")
    private LocalDateTime candleDateTimeKst;

    @JsonProperty("opening_price")
    private Double openingPrice;

    @JsonProperty("high_price")
    private Double highPrice;

    @JsonProperty("low_price")
    private Double lowPrice;

    @JsonProperty("trade_price")
    private Double tradePrice;

    @JsonProperty("timestamp")
    private Long timestamp;

    @JsonProperty("candle_acc_trade_price")
    private Double candleAccTradePrice;

    @JsonProperty("candle_acc_trade_volume")
    private Double candleAccTradeVolume;

    public LocalDateTime getTimestampAsLocalDateTime() {
        return LocalDateTime.ofInstant(Instant.ofEpochMilli(timestamp), ZoneId.of("UTC"));
    }

}
