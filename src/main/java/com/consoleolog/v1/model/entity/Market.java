package com.consoleolog.v1.model.entity;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import lombok.*;
import org.hibernate.annotations.CreationTimestamp;

import java.time.LocalDateTime;

@Builder
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@ToString
@Getter
@Entity
public class Market {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String ticker;

    private String interval;

    private Double price;

    private Double emaShort;

    private Double emaMid;

    private Double emaLong;

    private Integer stage;

    private Double macdUp;

    private Double macdMid;

    private Double macdLow;

    @CreationTimestamp
    private LocalDateTime createdAt;

}
