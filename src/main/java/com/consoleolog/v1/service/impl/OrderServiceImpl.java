package com.consoleolog.v1.service.impl;

import com.consoleolog.v1.common.component.UpbitComponent;

import com.consoleolog.v1.model.dto.OrderReqDto;
import com.consoleolog.v1.model.dto.OrderResDto;
import com.consoleolog.v1.model.dto.type.SideType;
import com.consoleolog.v1.model.entity.OrderHistory;
import com.consoleolog.v1.repository.OrderRepository;
import com.consoleolog.v1.service.OrderService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import java.security.NoSuchAlgorithmException;

@Slf4j
@RequiredArgsConstructor
@Service
public class OrderServiceImpl implements OrderService {

    private final OrderRepository orderRepository;

    private final UpbitComponent upbitComponent;

    @Override
    public OrderHistory executeOrder(OrderReqDto orderReqDto) throws NoSuchAlgorithmException {
        if (orderReqDto.getSide().equals(SideType.BUY)){
            log.info("""
            =========================================
            
                               BUY
            
            =========================================
            """);
        };
        if (orderReqDto.getSide().equals(SideType.SELL)){
            log.info("""
            =========================================
            
                               SELL
            
            =========================================
            """);
        }


        OrderResDto orderResDto = upbitComponent.createOrder(orderReqDto);

        log.info("""
            =========================================
            
            Result :  {}
            
            =========================================
            """, orderReqDto);

        OrderHistory order = OrderHistory.builder()
                .id(orderResDto.getIdentifier())
                .ticker(orderResDto.getMarket())
                .price(orderResDto.getLocked())
                .build();
        return orderRepository.save(order);
    }



}
