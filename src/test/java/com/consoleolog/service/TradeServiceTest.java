package com.consoleolog.service;

import com.consoleolog.v1.model.dto.CandleReqDto;
import com.consoleolog.v1.model.dto.CandleResDto;
import com.consoleolog.v1.model.dto.type.EmaType;
import com.consoleolog.v1.model.dto.type.IntervalType;
import com.consoleolog.v1.common.component.StrategyComponent;
import com.consoleolog.v1.common.component.UpbitComponent;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import java.util.ArrayList;
import java.util.List;

@SpringBootTest
public class TradeServiceTest {

    private final UpbitComponent upbitComponent;
    private final StrategyComponent strategyComponent;

    @Autowired
    public TradeServiceTest(
            UpbitComponent upbitComponent,
            StrategyComponent strategyComponent
    ){
        this.upbitComponent = upbitComponent;
        this.strategyComponent= strategyComponent;
    }

    @Test
    public void testCalMacdTest() {
        // CandleReqDto 객체 생성
        CandleReqDto candleReqDto = CandleReqDto
                .builder()
                .market("KRW-ETH")
                .interval(IntervalType.MINUTE)
                .unit(1)
                .build();

        // 캔들 데이터를 가져오기
        List<CandleResDto> candleResList = upbitComponent.getCandles(candleReqDto);

        // 종가 리스트 추출
        List<Double> prices = candleResList.stream().map(CandleResDto::getTradePrice).toList();

        // 단기, 중기, 장기 EMA 리스트 생성
        List<Double> emaShort = strategyComponent.createEmaList(EmaType.SHORT, prices);
        List<Double> emaMid = strategyComponent.createEmaList(EmaType.MID, prices);
        List<Double> emaLong = strategyComponent.createEmaList(EmaType.LONG, prices);

        // MACD 계산을 위한 리스트들
        List<Double> macdUpList = new ArrayList<>();
        List<Double> macdMidList = new ArrayList<>();
        List<Double> macdLowList = new ArrayList<>();

        // MACD Up (Short - Mid)
        for (int i = 0; i < emaMid.size(); i++) {
            double macdUp = emaShort.get(i) - emaMid.get(i);
            macdUpList.add(macdUp);
        }

        // MACD Mid (Mid - Long)
        for (int i = 0; i < emaLong.size(); i++) {
            double macdMid = emaShort.get(i) - emaLong.get(i);
            macdMidList.add(macdMid);
        }

        // MACD Low (Up - Mid)
        for (int i = 0; i < macdUpList.size(); i++) {
            double macdLow = emaMid.get(i) - emaLong.get(i);
            macdLowList.add(macdLow);
        }

        // 결과 출력
        System.out.println("MACD Up List: " + macdUpList);
        System.out.println("MACD Mid List: " + macdMidList);
        System.out.println("MACD Low List: " + macdLowList);
    }

    @Test
    public void testCalEma(){
        /*
         * EMA = 현재 가격 * k + ( 전날 가격 * (1 - k) )
         * k = 1 / (1 + (day - 1)) 업비트
         * */

        CandleReqDto candleReqDto = CandleReqDto
                .builder()
                .market("KRW-BTC")
                .interval(IntervalType.DAY)
                .count(5)  // 5일 간의 데이터 가져오기
                .build();

        List<CandleResDto> candleResList = upbitComponent.getCandles(candleReqDto);

        // day는 60으로 설정 (예시로)
        double day = 60;

        // k 계산
//        double K = 1 / (1 + (day - 1));

        double K = 2.0 / ( day + 1 );

        for (int i = 0; i < candleResList.size() - 1; i++) {
            double ema = candleResList.get(i).getTradePrice() * K + ( candleResList.get(i + 1).getTradePrice() * ( 1 - K ) );
            System.out.println(ema);
        }
//        for (CandleResDto candleResDto : candleResList) {
//            double ema = candleResDto.getTradePrice() * K + (  )
//
//
//        }

//        // 가격만 추출
//        List<Double> prices = candleResList.stream().map(CandleResDto::getTradePrice).toList();
//
//
//
//        // 첫 번째 EMA를 초기화할 때, 첫 번째 가격을 그대로 사용할 수 있음
//        double ema = prices.get(0);  // 첫 번째 가격을 기준으로 초기화
//
//        // 2일 차부터 EMA 계산 시작
//        for (int i = 1; i < prices.size(); i++) {
//            ema = prices.get(i) * K + (ema * (1 - K));
//            System.out.println("EMA Day " + (i + 1) + ": " + ema);
//        }
//
//        // 최종 EMA 출력
//        System.out.println("Final EMA: " + ema);
    }

    @Test
    public void testdsad(){
        CandleReqDto candleReqDto = CandleReqDto
                .builder()
                .market("KRW-BTC")
                .interval(IntervalType.DAY)
                .count(5)  // 5일 간의 데이터 가져오기
                .build();

        List<CandleResDto> candleResList = upbitComponent.getCandles(candleReqDto);
        List<Double> prices = candleResList.stream().map(CandleResDto::getTradePrice).toList();
        double day = 60;
        double K = 2.0 / ( day + 1 );
        double ema = prices.get(0) + ( Math.pow(1 + K, 2) * prices.get(1) ) + Math.pow(1 + K, 3) * prices.get(2);

        for (int i = 2; i < day; i++) {
            Math.pow(1 + K , 2);
        }


    }

    @Test
    public void test() {
        // CandleReqDto 설정
        CandleReqDto candleReqDto = CandleReqDto
                .builder()
                .market("KRW-BTC")
                .interval(IntervalType.DAY)
                .count(200)  // 5일 간의 데이터 가져오기
                .build();

        // 업비트 API에서 캔들 데이터 가져오기
        List<CandleResDto> candleResList = upbitComponent.getCandles(candleReqDto);
        System.out.println(candleResList.get(0));
        System.out.println(candleResList.get(1));
        System.out.println(candleResList.get(2));

        // 종가 데이터 가져오기
        List<Double> prices = candleResList.stream().map(CandleResDto::getTradePrice).toList();
        System.out.println(prices.get(0));
        int period = 60;

        double sma = 0.0;
        for (int i = 0; i < period; i++) {
            sma += prices.get(i);
        }
        sma /= period;

        System.out.println(sma);

        double k = 1.0 / ( 1 + (period - 1));
//        k = 1 / (1 + (day - 1)) 업비트
        double ema = sma;
        // EMA 계산
        for (int i = 1; i < prices.size(); i++) {
            ema = (prices.get(i) * k) + (ema * (1 - k));
            System.out.println(ema);
        }
        System.out.println(ema);
    }
}
