package com.consoleolog.v1.common.component;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;
import com.consoleolog.global.config.AppProperties;
import com.consoleolog.v1.model.dto.*;
import com.consoleolog.v1.model.dto.type.IntervalType;
import com.consoleolog.v1.model.dto.type.OrderType;
import com.consoleolog.v1.model.dto.type.SideType;

import com.fasterxml.jackson.module.paramnames.ParameterNamesModule;
import com.google.gson.Gson;
import lombok.RequiredArgsConstructor;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.math.BigInteger;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.*;

@RequiredArgsConstructor
@Service
public class UpbitComponent {

    private final AppProperties appProperties;
    private final RestTemplate restTemplate;
    private final ParameterNamesModule parameterNamesModule;

    private String getAccessKey(){
        return appProperties.getUpbit().getAccessKey();
    }
    private String getSecretKey(){
        return appProperties.getUpbit().getSecretKey();
    }
    private String getServerUrl(){
        return appProperties.getUpbit().getServerUrl();
    }

    public List<CurrencyDto> getCurrencies(){
        Algorithm algorithm = Algorithm.HMAC256(appProperties.getUpbit().getSecretKey());
        String jwtToken = JWT.create()
                .withClaim("access_key", getAccessKey())
                .withClaim("nonce", UUID.randomUUID().toString())
                .sign(algorithm);
        String authToken = "Bearer " + jwtToken;

        try {
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            headers.set("Authorization", authToken);

            HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(headers);

            ResponseEntity<List<CurrencyDto>> response = restTemplate.exchange(
                    getServerUrl() + "/v1/accounts",
                    HttpMethod.GET,
                    entity,
                    new ParameterizedTypeReference<>() {}
            );

            return response.getBody();
        } catch (Exception e){
            e.printStackTrace();
            throw new RuntimeException(e);
        }
    }

    public CurrencyDto getCurrency(String currency){
        List<CurrencyDto> currencies = getCurrencies();

        for (CurrencyDto c : currencies) {
            if (c.getCurrency().equals(currency)) {
                return c;
            }
        }
        throw new RuntimeException("Currency not found");
    }

    public OrderResDto createOrder(OrderReqDto orderReqDto) throws NoSuchAlgorithmException {

        Map<String, Object> params = createOrdParams(orderReqDto);

        List<String> queryElements = new ArrayList<>();

        for( Map.Entry<String, Object> entity : params.entrySet()) {
            queryElements.add(entity.getKey() + "=" + entity.getValue());
        }

        String queryString = String.join("&", queryElements.toArray(new String[0]));

        MessageDigest md = MessageDigest.getInstance("SHA-512");
        md.update(queryString.getBytes(StandardCharsets.UTF_8));

        String queryHash = String.format("%0128x", new BigInteger(1, md.digest()));
        Algorithm algorithm = Algorithm.HMAC256(getSecretKey());
        String jwtToken = JWT.create()
                .withClaim("access_key", getAccessKey())
                .withClaim("nonce", UUID.randomUUID().toString())
                .withClaim("query_hash", queryHash)
                .withClaim("query_ash_alg", "SHA512")
                .sign(algorithm);
        String authToken = "Bearer " + jwtToken;

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", authToken);

        String jsonParams = new Gson().toJson(params);

        HttpEntity<String> entity = new HttpEntity<>(jsonParams, headers);
        ResponseEntity<OrderResDto> response = restTemplate.exchange(
                getServerUrl() + "/v1/orders",
                HttpMethod.POST,
                entity,
                new ParameterizedTypeReference<>() {}
        );

        return response.getBody();
    }

    private Map<String, Object> createOrdParams(OrderReqDto orderReqDto) {
        Map<String, Object> params = new HashMap<>();

        params.put("market", orderReqDto.getMarket());
        params.put("side", orderReqDto.getSide().getValue());
        params.put("ord_type", orderReqDto.getOrderType().getValue());
        if (SideType.BUY.equals(orderReqDto.getSide())) {
            params.put("price", orderReqDto.getPrice());
        }
        else if (SideType.SELL.equals(orderReqDto.getSide())){
            params.put("volume", orderReqDto.getVolume());
        }

        if (OrderType.LIMIT.equals(orderReqDto.getOrderType()) || OrderType.BEST.equals(orderReqDto.getOrderType())) {
            params.put("time_in_force", orderReqDto.getTimeInForce());
        }
        if (orderReqDto.getIdentifier() != null) {
            params.put("identifier", orderReqDto.getIdentifier());
        }
        return params;
    }


    public List<CandleResDto> getCandles(CandleReqDto candleReqDto) {

        String url = createUrl(candleReqDto);

        HttpHeaders headers = new HttpHeaders();
        headers.add("accept", "application/json");

        HttpEntity<MultiValueMap<String, Object>> entity = new HttpEntity<>(headers);

        ResponseEntity<List<CandleResDto>> response = restTemplate.exchange(
                url,
                HttpMethod.GET,
                entity,
                new ParameterizedTypeReference<List<CandleResDto>>() {}
        );
        return response.getBody();
    }

    private String createUrl(CandleReqDto candleReqDto) {
        String market = "?market=" + candleReqDto.getMarket();
        String count = "&count=" + candleReqDto.getCount().toString();
        String interval = "days";
        if (IntervalType.MINUTE.equals(candleReqDto.getInterval())) {
            interval = candleReqDto.getInterval().getValue() + "/" + candleReqDto.getUnit().toString();
        }

        String to = "";
        if (candleReqDto.getTo() != null) {
            to = "&to" + candleReqDto.getTo();
        }

        return getServerUrl() + "/v1/candles/" + interval + market + count + to;
    }
}
