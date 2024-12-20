package com.consoleolog.global.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;

@Getter
@ConfigurationProperties(prefix = "app")
public class AppProperties {

    private final Upbit upbit = new Upbit();

    @Setter
    @Getter
    public static class Upbit {
        private String accessKey;
        private String secretKey;
        private String serverUrl;
    }


}
