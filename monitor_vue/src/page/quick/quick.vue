<template>
  <div class="quick-container">
    <el-card class="quick-card">
      <v-chart ref="chart1" :options="option" />
    </el-card>
  </div>
</template>

<script>
import ECharts from "vue-echarts";
import "echarts/lib/chart/line";
import "echarts/lib/component/polar";

var chart1_data = [];

var local_now = +new Date();
for (var i = 3; i > 0; i--) {
  var cur_date = new Date(local_now - i * 1000);

  chart1_data.push({
    name: cur_date.toString(),
    value: [
      [cur_date.getFullYear(), cur_date.getMonth(), cur_date.getDate()].join(
        "/"
      ) +
        " " +
        [
          cur_date.getHours(),
          cur_date.getMinutes(),
          cur_date.getSeconds(),
        ].join(":"),
      0,
    ],
  });
}

export default {
  components: {
    "v-chart": ECharts,
  },

  data() {
    return {
      option: {
        title: {
          text: "匹配时间(平均值)/ms",
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              [now.getHours(), now.getMinutes(), now.getSeconds()].join(":") +
              " " +
              params.value[1]
            );
          },
          axisPointer: {
            animation: false,
          },
        },
        xAxis: {
          type: "time",
          splitLine: {
            show: true,
          },
          axisLabel: {
            formatter: function (value, index) {
              var date = new Date(value);
              return (
                // [date.getMonth(), date.getDate()].join("/") +
                // " " +
                [date.getHours(), date.getMinutes(), date.getSeconds()].join(
                  ":"
                )
              );
            },
          },
        },
        yAxis: {
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: true,
          },
        },
        series: [
          {
            connectNulls: true,
            name: "模拟数据",
            type: "line",
            showSymbol: false,
            hoverAnimation: false,
            data: chart1_data,
          },
        ],
      },
    };
  },
  created() {},

  methods: {},

  mounted() {
    const that = this;

    setInterval(function () {
      that.$axios
        // .get(`${window.$config.HOST}/api/getMatchTime`)
        .get(`/api/getMatchTime`)
        .then((response) => {
          if (chart1_data.length == 60) {
            chart1_data.shift();
          }
          var cur_date = new Date();
          chart1_data.push({
            name: cur_date.toString(),
            value: [
              [
                cur_date.getFullYear(),
                cur_date.getMonth(),
                cur_date.getDate(),
              ].join("/") +
                " " +
                [
                  cur_date.getHours(),
                  cur_date.getMinutes(),
                  cur_date.getSeconds(),
                ].join(":"),
              response.data.average,
            ],
          });
        })
        .catch((error) => {
          console.lof(error);
        });
    }, 1000);
  },
};
</script>

<style lang="less">
.quick-container {
  .quick-card {
    .el-card__header {
      padding: 0 20px;
      height: 48px;
      line-height: 48px;
    }
    .el-step__description {
      margin-top: 15px;
      p {
        line-height: 1.5;
      }
    }
  }
}
</style>