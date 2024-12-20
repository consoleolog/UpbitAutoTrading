package com.consoleolog.v1.model.dto;

import com.consoleolog.v1.model.dto.type.OrderType;
import com.consoleolog.v1.model.dto.type.SideType;
import lombok.Builder;
import lombok.Getter;
import lombok.ToString;

@Builder
@ToString
@Getter
public class OrderReqDto {

    private String market;

    private SideType side;

    private Double volume;

    private Double price;

    private OrderType orderType;

    private String identifier;

    private String timeInForce;

    private OrderReqDto(String market, SideType side, Double volume, Double price, OrderType orderType, String identifier, String timeInForce) {
        this.market = market;
        this.side = side;
        this.volume = volume;
        this.price = price;
        this.orderType = orderType;
        this.identifier = identifier;
        this.timeInForce = timeInForce;
    }


}
