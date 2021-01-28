package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"strings"
)

// azure mysql의 슬로우 로그 파일을 패러미터로 주고서 실행
// time, user, duration, rows, sql 을 csv 파일 형태로 출력함.
// excel 에서 슬로우 쿼리 내용 확인하기 

func main() {

	var filename string
	var v_time, v_user, v_duration, v_rows, v_sql string

	flag.Parse()
	args := flag.Args()

	if len(args) < 1 {
		filename = "d:/Downloads/test.txt"
	} else {
		filename = args[0]
	}
	file1, _ := os.Open(filename)
	defer file1.Close()

	scanner := bufio.NewScanner(file1)

	sql_line := -1
	v_time = ""
	v_user = ""
	v_duration = ""
	v_rows = ""
	v_sql = ""

	fmt.Println("time, user, duration, rows, sql")
	for scanner.Scan() {
		s := scanner.Text()

		if len(s) > 0 {
			switch {

			case s[0] == '#' && strings.Index(s, "Time") > -1:
				if v_time != "" {
					fmt.Println(v_time, ",", v_user, ",", v_duration, ",", v_rows, ",", v_sql)
				}
				v_time = s[8:27]
				sql_line = 0
			case s[0] == '#' && strings.Index(s, "User@Host") > -1:
				idx := strings.Index(s, " @ ")
				v_user = s[13:idx]
			case s[0] == '#' && strings.Index(s, "Query_time") > -1:
				idx := strings.Index(s, " Lock_time")
				v_duration = s[14:idx]

				idx = strings.Index(s, "Rows_examined:")
				v_rows = s[idx+14 : len(s)]
				sql_line = 1
			case s[0] != '#':
				if sql_line == 1 {
					v_sql = ""
				} else if sql_line == 3 || sql_line == 4 {
					v_sql = v_sql + s[0:len(s)-1]
					//fmt.Println("vsql ==>", v_sql)
				}
				sql_line++

			}
		}

	}
	fmt.Println(v_time, ",", v_user, ",", v_duration, ",", v_rows, ",", v_sql)

}
