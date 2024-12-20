package com.consoleolog.v1.model.entity;

import jakarta.persistence.Entity;
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
public class OrderHistory {

    @Id
    private String id;

    private String ticker;

    private Double price;

    @CreationTimestamp
    private LocalDateTime createdAt;

}
