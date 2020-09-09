<template>
  <div class="quick-container">
    <el-card class="quick-card">
      <v-chart :options="option" />
    </el-card>
  </div>
</template>

<script>
import { Card, Steps, Step, Button } from "element-ui";
import ECharts from "vue-echarts";
import "echarts/lib/chart/line";
// import "echarts/lib/component/polar";

var local_pic_data = [];
var local_now = +new Date(1997, 9, 3);
var local_oneDay = 24 * 3600 * 1000;
var local_value = Math.random() * 1000;
function randomData() {
  local_now = new Date(+local_now + local_oneDay);
  local_value = local_value + Math.random() * 21 - 10;
  return {
    name: local_now.toString(),
    value: [
      [
        local_now.getFullYear(),
        local_now.getMonth() + 1,
        local_now.getDate(),
      ].join("/"),
      Math.round(local_value),
    ],
  };
}

for (var i = 0; i < 1000; i++) {
  local_pic_data.push(randomData());
}

export default {
  components: {
    ElCard: Card,
    ElSteps: Steps,
    ElStep: Step,
    ElButton: Button,
    "v-chart": ECharts,
  },

  data() {
    return {
      option: {
        title: {
          text: "动态数据 + 时间坐标轴",
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              date.getDate() +
              "/" +
              (date.getMonth() + 1) +
              "/" +
              date.getFullYear() +
              " : " +
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
            show: false,
          },
        },
        yAxis: {
          type: "value",
          boundaryGap: [0, "100%"],
          splitLine: {
            show: false,
          },
        },
        series: [
          {
            name: "模拟数据",
            type: "line",
            showSymbol: false,
            hoverAnimation: true,
            data: local_pic_data,
          },
        ],
      },
    };
  },
  created() {},

  methods: {
    
  },
  mounted() {
    setInterval(function () {
      for (var i = 0; i < 5; i++) {
        local_pic_data.shift();
        local_pic_data.push({
          name: local_now.toString(),
          value: [
            [
              local_now.getFullYear(),
              local_now.getMonth() + 1,
              local_now.getDate(),
            ].join("/"),
            Math.round(local_value),
          ],
        });
      }
      // console.log(this.option);
      this.option = this.pic_data;
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