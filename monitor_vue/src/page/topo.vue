<template>
  <div class="quick-container">
    <el-card class="quick-card">
      <v-chart ref="chart2" :options="option2" />
    </el-card>
  </div>
</template>

<script>
import ECharts from "vue-echarts";
// import "echarts/lib/chart/line";
// import "echarts/lib/component/polar";
import echarts from "echarts";

var data2 = [
  {
    symbolSize: 20,
    id: 0,
    name: "super",
  },
  {
    id: 1,
    symbolSize: 20,
    name: "edge1",
  },
  {
    id: 2,
    symbolSize: 20,
    name: "edge2",
  },
  {
    id: 3,
    symbolSize: 20,
    name: "edge3",
  },
];

var edges2 = [
  {
    source: 0,
    target: 1,
    lineStyle: {
      width: 5,
      curveness: 0.2,
    },
  },
  {
    source: 0,
    target: 2,
    lineStyle: {
      width: 5,
      curveness: 0.2,
    },
  },
  {
    source: 0,
    target: 3,
    lineStyle: {
      width: 5,
      curveness: 0.2,
    },
  },
];

export default {
  components: {
    "v-chart": ECharts,
  },

  data() {
    return {
      option2: {
        grid:{
          top:'14%',
          bottom:'18%',
          left:'15%',
          right:'4%',
        },
        series: [
          {
            type: "graph",
            layout: "force",
            animation: false,
            data: data2,
            force: {
              // repulsion: 200,
              edgeLength: 300,
            },
            edgeSymbolSize: 1200,
            edges: edges2,
          },
        ],
      },
    };
  },
  created() {},

  methods: {},

  mounted() {
    const that = this;
  }
};
</script>

<style lang="less" scoped>
.quick-container {
  .quick-card {
    height:80vh;
    .echarts{
      width:100%;
      height:750px;
    }
    .el-card__header {
      padding: 0 20px;
      height: 48px;
      line-height: 48px;
    }
    .el-card__body{
      height:100%;
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