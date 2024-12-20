package com.consoleolog.v1.model.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.ToString;

@ToString
@Getter
public class CurrencyDto {

    @JsonProperty("currency")
    private String currency;

    @JsonProperty("balance")
    private Double balance;

    @JsonProperty("locked")
    private Double locked;

    @JsonProperty("avg_buy_price")
    private Double avgBuyPrice;

    @JsonProperty("avg_buy_price_modified")
    private Boolean avgBuyPriceModified;

    @JsonProperty("unit_currency")
    private String unitCurrency;

}
