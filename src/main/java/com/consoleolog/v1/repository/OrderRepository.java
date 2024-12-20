package com.consoleolog.v1.repository;

import com.consoleolog.v1.model.entity.OrderHistory;
import org.springframework.data.jpa.repository.JpaRepository;

public interface OrderRepository extends JpaRepository<OrderHistory, String> {
}
