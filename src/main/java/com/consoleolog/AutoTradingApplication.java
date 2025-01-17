package com.consoleolog;

import com.consoleolog.global.config.AppProperties;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.scheduling.annotation.EnableScheduling;

@EnableScheduling
@EnableConfigurationProperties(AppProperties.class)
@SpringBootApplication
public class AutoTradingApplication {

    public static void main(String[] args) {
        SpringApplication.run(AutoTradingApplication.class, args);
    }

}
