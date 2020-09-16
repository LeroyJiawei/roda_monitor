<template>
  <div class="n2n-container">
    <el-card>
      <v-chart ref="chart2" :options="option2" />
    </el-card>
  <el-card style="margin-top:20px">
    <el-button type="primary" style="margin:10px 0;">新增节点</el-button>
    <el-table
    :data="tableData"
    style="width: 100%"
    max-height="250">
    <el-table-column
      prop="role"
      label="角色"
      >
      </el-table-column>
    <el-table-column
      prop="name"
      label="名称"
      >
    
    
    </el-table-column>
    <el-table-column
      prop="vlan_ip"
      label="vlan IP"
      >
    </el-table-column>
    <el-table-column
      prop="uncertain"
      label="待定"
      >
    </el-table-column>

    
    <el-table-column
      label="操作"
    >
      <template slot-scope="scope">
        <el-button
          @click.native.prevent=""
          type="text"
          size="small">
          修改
        </el-button>
        <el-button
          @click.native.prevent="deleteRow(scope.$index, tableData)"
          type="text"
          size="small">
          删除
        </el-button>
      </template>
    </el-table-column>
  </el-table>
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
      tableData: [{
          name: '王小虎',
          rol:'',
          vlan_ip: '普陀区',
          uncertain: '...',
        }],
      option2: {
        grid:{
          top:'14%',
          bottom:'10%',
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

<style>

</style>