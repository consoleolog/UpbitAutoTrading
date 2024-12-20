package com.consoleolog.v1.repository;

import com.consoleolog.v1.model.entity.Market;
import org.springframework.data.jpa.repository.JpaRepository;

public interface MarketRepository extends JpaRepository<Market, Long> {
}
