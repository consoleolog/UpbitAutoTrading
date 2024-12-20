package com.consoleolog.v1.service;

import com.consoleolog.v1.model.dto.OrderReqDto;
import com.consoleolog.v1.model.entity.OrderHistory;

import java.security.NoSuchAlgorithmException;

public interface OrderService {
    OrderHistory executeOrder(OrderReqDto orderReqDto) throws NoSuchAlgorithmException;
}
