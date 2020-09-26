<template>
  <div class="container">
    <el-card class="box-card">
      <div class="deploy-info">
        <el-radio-group v-model="filterRadio" @change="radioChange">
          <el-radio-button
            v-for="(item, index) in filterList"
            :key="index"
            :label="item.name"
          ></el-radio-button>
        </el-radio-group>
      </div>

      <div class="deploy-info">
        <h1>配置信息</h1>
        <el-table :data="filterChoose" border style="width: 100%">
          <el-table-column prop="network_name" label="网络名">
          </el-table-column>
          <el-table-column prop="source_data_system" label="源类型">
          </el-table-column>
          <el-table-column prop="source_info" label="源配置"> </el-table-column>
          <el-table-column prop="state" label="状态"> </el-table-column>
        </el-table>
      </div>
    </el-card>

    <el-card class="charts" style="margin-top: 20px">
      <div class="left">
        <v-chart class="item" ref="chart1" :options="chart1Option" />
        <v-chart class="item" ref="chart2" :options="chart2Option" />
      </div>
      <div class="right">
        <v-chart class="item" ref="chart3" :options="chart3Option" />
        <v-chart class="item" ref="chart4" :options="chart4Option" />
      </div>
    </el-card>
  </div>
</template>

<script>
import ECharts from "vue-echarts";
import echarts from "echarts";

var chart1_data = [];
var chart2_data = [];
var chart3_data = [];
var chart4_data = [];

export default {
  components: {
    "v-chart": ECharts,
  },
  data() {
    return {
      filterRadio: null,
      filterList: [],
      filterChoose: [],

      intervalId: null,

      chart1Option: {
        title: {
          text: "匹配时间(平均值)/ms",
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              [date.getHours(), date.getMinutes(), date.getSeconds()].join(
                ":"
              ) +
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
              return [
                date.getHours(),
                date.getMinutes(),
                date.getSeconds(),
              ].join(":");
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
      chart2Option: {
        title: {
          text: "匹配时间(最大值)/ms",
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              [date.getHours(), date.getMinutes(), date.getSeconds()].join(
                ":"
              ) +
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
              return [
                date.getHours(),
                date.getMinutes(),
                date.getSeconds(),
              ].join(":");
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
            data: chart2_data,
          },
        ],
      },
      chart3Option: {
        title: {
          text: "匹配时间(最小值)/ms",
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              [date.getHours(), date.getMinutes(), date.getSeconds()].join(
                ":"
              ) +
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
              return [
                date.getHours(),
                date.getMinutes(),
                date.getSeconds(),
              ].join(":");
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
            data: chart3_data,
          },
        ],
      },
      chart4Option: {
        title: {
          text: "匹配时间(方差)",
        },
        tooltip: {
          trigger: "axis",
          formatter: function (params) {
            params = params[0];
            var date = new Date(params.name);
            return (
              [date.getHours(), date.getMinutes(), date.getSeconds()].join(
                ":"
              ) +
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
              return [
                date.getHours(),
                date.getMinutes(),
                date.getSeconds(),
              ].join(":");
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
            data: chart4_data,
          },
        ],
      },
    };
  },
  created() {
    this.$axios
      .get(`${window.$config.HOST}/api/filter/list`)
      .then((response) => {
        if (response.data.status === "OK") {
          this.filterList = response.data.data;
          if (this.filterList.length > 0) {
            this.filterRadio = this.filterList[0].name;
            this.filterChoose = [this.filterList[0]];
          }
        } else {
          console.log("get list failed");
        }
      });
  },
  mounted() {
    const that = this;

    that.intervalId = setInterval(function () {
      that.$axios
        .get(`${window.$config.HOST}/api/filter/match_perf`, {
          params: {
            filter_id: that.filterChoose[0].id,
            addr: that.filterChoose[0].addr,
          },
        })
        .then((response) => {
          var getData = response.data.data;
          if (chart1_data.length == 60) {
            chart1_data.shift();
            chart2_data.shift();
            chart3_data.shift();
            chart4_data.shift();
          }
          var cur_date = new Date();
          var date_val =
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
            ].join(":");
          chart1_data.push({
            name: cur_date.toString(),
            value: [date_val, getData.average],
          });
          chart2_data.push({
            name: cur_date.toString(),
            value: [date_val, getData.maximum],
          });
          chart3_data.push({
            name: cur_date.toString(),
            value: [date_val, getData.minimum],
          });
          chart4_data.push({
            name: cur_date.toString(),
            value: [date_val, getData.variance],
          });
        })
        .catch((error) => {
          console.log(error);
        });
    }, 1000);
  },
  methods: {
    radioChange(val) {
      this.filterList.forEach((ele) => {
        if (ele.name === val) {
          this.filterChoose = [ele];
        }
      });
      // chart1_data = [];
    },
  },
};
</script>

<style scoped>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 200px;
  min-height: 400px;
}
h1 {
  font-size: 24px;
  /* text-align:center; */
  margin-bottom: 10px;
}
.deploy-info {
  padding: 20px 50px;
}
.box-card {
  width: 100%;
  margin: 0 auto;
}

.charts {
  display: flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
}

.left {
  flex: 1;
  display: inline-block;
}

.right {
  flex: 1;
}

.item {
  display: inline-block;
}
</style>