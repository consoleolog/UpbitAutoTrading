package com.consoleolog.v1.model.dto;

import com.consoleolog.v1.model.dto.type.OrderType;
import com.consoleolog.v1.model.dto.type.SideType;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Getter;
import lombok.ToString;

import java.time.LocalDateTime;
import java.time.OffsetDateTime;

@ToString
@Getter
public class OrderResDto {

    @JsonProperty("uuid")
    private String uuid;

    @JsonProperty("side")
    private SideType side;

    @JsonProperty("ord_type")
    private OrderType orderType;

    @JsonProperty("price")
    private Double price;

    @JsonProperty("state")
    private String state;

    @JsonProperty("market")
    private String market;

    @JsonProperty("created_at")
    private String createdAt;

    @JsonProperty("volume")
    private Double volume;

    @JsonProperty("remaining_volume")
    private Double remainingVolume;

    @JsonProperty("reserved_fee")
    private Double reservedFee;

    @JsonProperty("remaining_fee")
    private Double remainingFee;

    @JsonProperty("paid_fee")
    private Double paidFee;

    @JsonProperty("locked")
    private Double locked;

    @JsonProperty("executed_volume")
    private Double executedVolume;

    @JsonProperty("trades_count")
    private Integer tradesCount;

    @JsonProperty("time_in_force")
    private String timeInForce;

    @JsonProperty("identifier")
    private String identifier;

}
