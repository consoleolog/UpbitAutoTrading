package com.consoleolog.service;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;

import com.consoleolog.global.config.AppProperties;
import com.consoleolog.v1.model.dto.CandleResDto;
import com.consoleolog.v1.model.dto.CurrencyDto;
import lombok.extern.slf4j.Slf4j;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;


import java.util.List;
import java.util.Objects;
import java.util.UUID;

@Slf4j
@SpringBootTest
public class UpbitApiTest {

    private final AppProperties appProperties;
    private final RestTemplate restTemplate;
    @Autowired
    public UpbitApiTest(
            AppProperties appProperties,
            RestTemplate restTemplate
    ) {
        this.appProperties = appProperties;
        this.restTemplate = restTemplate;
    }

    @Test
    public void testGetCurrencies(){

        String accessKey = appProperties.getUpbit().getAccessKey();
        String secretKey = appProperties.getUpbit().getSecretKey();
        String serverUrl = appProperties.getUpbit().getServerUrl();

        Algorithm algorithm = Algorithm.HMAC256(secretKey);
        String jwtToken = JWT.create()
                .withClaim("access_key", accessKey)
                .withClaim("nonce", UUID.randomUUID().toString())
                .sign(algorithm);

        String authenticationToken = "Bearer " + jwtToken;

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", authenticationToken);

            HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(headers);

            ResponseEntity<List<CurrencyDto>> response = restTemplate.exchange(
                    serverUrl + "/v1/accounts",
                    HttpMethod.GET,
                    entity,
                    new ParameterizedTypeReference<>() {}
            );

            System.out.println(response.getBody());

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testGetCurrency(){
        String accessKey = appProperties.getUpbit().getAccessKey();
        String secretKey = appProperties.getUpbit().getSecretKey();
        String serverUrl = appProperties.getUpbit().getServerUrl();

        Algorithm algorithm = Algorithm.HMAC256(secretKey);
        String jwtToken = JWT.create()
                .withClaim("access_key", accessKey)
                .withClaim("nonce", UUID.randomUUID().toString())
                .sign(algorithm);

        String authenticationToken = "Bearer " + jwtToken;

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", authenticationToken);

            HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(headers);

            ResponseEntity<List<CurrencyDto>> response = restTemplate.exchange(
                    serverUrl + "/v1/accounts",
                    HttpMethod.GET,
                    entity,
                    new ParameterizedTypeReference<>() {}
            );

            Objects.requireNonNull(response.getBody()).stream().map(c -> {
               if (c.getCurrency().equals("KRW")){
                   System.out.println(c.toString());
               }
                return null;
            });

        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    @Test
    public void testGetCandles(){
        String accessKey = appProperties.getUpbit().getAccessKey();
        String secretKey = appProperties.getUpbit().getSecretKey();
        String serverUrl = appProperties.getUpbit().getServerUrl();

        String url = serverUrl + "/v1/candles/seconds?count=1&market=KRW-BTC";

        HttpHeaders headers = new HttpHeaders();
        headers.add("accept", "application/json");

        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(headers);
        ResponseEntity<List<CandleResDto>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                entity,
                new ParameterizedTypeReference<>() {}
        );

        System.out.println(response.getBody());

    }

}
