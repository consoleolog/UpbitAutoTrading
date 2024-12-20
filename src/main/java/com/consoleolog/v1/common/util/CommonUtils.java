package com.consoleolog.v1.common.util;

import com.consoleolog.v1.model.dto.EmaListDto;

import java.text.SimpleDateFormat;
import java.util.Date;

public class CommonUtils {

    public static Integer getStage(EmaListDto emaListDto){
        double emaShort = emaListDto.getEmaShortList().get(0);
        double emaMid = emaListDto.getEmaMidList().get(0);
        double emaLong = emaListDto.getEmaLongList().get(0);

        if (emaShort > emaMid && emaMid > emaLong) {
            return 1;
        } else if (emaMid > emaShort && emaShort > emaLong) {
            return 2;
        } else if (emaMid > emaLong && emaLong > emaShort){
            return 3;
        } else if (emaLong > emaMid && emaMid > emaShort){
            return 4;
        } else if (emaLong > emaShort && emaShort > emaMid){
            return 5;
        } else if (emaShort > emaLong && emaLong > emaMid){
            return 6;
        } else {
            throw new RuntimeException();
        }
    }

    public static String createRandomDateString(){
        SimpleDateFormat simpleDateFormat = new SimpleDateFormat("yyyyMMddHHmmss");
        Date now = new Date();
        return simpleDateFormat.format(now);
    }

}
