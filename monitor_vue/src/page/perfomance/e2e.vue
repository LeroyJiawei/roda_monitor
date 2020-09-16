<template>
  <div class="container">
  <el-card class="box-card">
    <div class="deploy-info">
      <h1>配置信息</h1>
      <el-table
    :data="tableData"
    border
    style="width: 100%">
    <el-table-column
      prop="vlan_ip"
      label="vlan ip"
      width="200"
      >
    </el-table-column>
    <el-table-column
      prop="deploy1"
      label="配置1"
      >
    </el-table-column>
    <el-table-column
      prop="deploy2"
      label="配置2">
    </el-table-column>
    <el-table-column
      prop="deploy3"
      label="配置3">
    </el-table-column>
  </el-table>
    </div>
  </el-card>
  <el-card class="charts" style="margin-top:20px;">
    <div class="left">
      <v-chart  class="item" ref="chart2" :options="line" />
      <v-chart class="item" ref="chart2" :options="line" /> 
    </div>
    <div class="right">
      <v-chart class="item" ref="chart2" :options="line" />
      <v-chart class="item" ref="chart2" :options="line" />
    </div>
  </el-card>
  </div>
</template>

<script>
import ECharts from "vue-echarts";
// import "echarts/lib/chart/line";
// import "echarts/lib/component/polar";
import echarts from "echarts";
export default {
  components: {
    "v-chart": ECharts,
  },
  data(){
    return{
      tableData: [{
          name: '王小虎',
          deploy1:'',
          deploy2:'',
          deploy3:'',

        }],
      line:{
    xAxis: {
        type: 'category',
        data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    },
    yAxis: {
        type: 'value'
    },
    series: [{
        data: [820, 932, 901, 934, 1290, 1330, 1320],
        type: 'line',
        smooth: true
    }]
}
    }
  },
  methods: {
    
    }

}
</script>

<style scoped>

.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
h1{
    font-size:24px;
    /* text-align:center; */
    margin-bottom:10px;
}
.deploy-info{
    padding:0 50px;
}
.box-card {
    width: 100%;
    margin:0 auto;
  }

.charts{
  display:flex;
  align-items: center;
  flex-direction: row;
  justify-content: center;
}

.left{
  flex:1;
  display:inline-block;
}

.right{
  flex:1;
}

.item{
  display:inline-block;
}


</style>