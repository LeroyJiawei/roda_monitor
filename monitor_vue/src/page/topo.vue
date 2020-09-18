<template>
  <div class="quick-container">
    <el-card class="quick-card">
      <v-chart ref="chart2" :options="option2" id="tpc" />
    </el-card>


    <el-card style="margin-top:20px">

      <el-table :data="tableData" style="width: 100%" max-height="2500">
        <el-table-column prop="rol" label="角色">
        </el-table-column>

        <el-table-column prop="name" label="名称">
        </el-table-column>

        <el-table-column prop="vlan_ip" label="vlan IP">
        </el-table-column>


        <el-table-column prop="vlan_name" label="vlan 名称">
        </el-table-column>

        <el-table-column prop="service_port" label="服务端口">
        </el-table-column>

        <el-table-column prop="supernode_name" label="超节点名称">
        </el-table-column>

        <el-table-column prop="create_time" label="创建时间">
        </el-table-column>

        <el-table-column prop="update_time" label="更新时间">
        </el-table-column>

        <el-table-column prop="state" label="状态">
        </el-table-column>

        <el-table-column prop="addr" label="地址">
        </el-table-column>

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
          rol: 'sink',
          name: '王小虎',
          vlan_ip: '1.1.1.1',
          vlan_name:'v1',
          service_port:50,
          supernode_name:'n1',
          create_time:'2020-9-14',
          update_time:'2020-9-15',
          state:'open',
          addr:'129号'
        }],
        option2: {
          grid: {
            top: '14%',
            bottom: '18%',
            left: '15%',
            right: '4%',
          },
          series: [
            {
              type: "graph",
              layout: "force",
              animation: true,
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
    created() {

    },

    methods: {
      getTopoData() {
        const _this = this
        this.$axios
          .get(`${window.$config.HOST}/api/n2n/topo`)
          .then((response) => {

            _this.data2 = response.data.data.nodes;
            _this.edges2 = response.data.data.edges;

            var optionOfTopo = {
              title: {
                show: true,
                text: '系统拓扑图',
                subtext: 'source和sink节点',
                left: "auto",
                top: "auto",
              },
              grid: {
                top: '14%',
                bottom: '18%',
                left: '15%',
                right: '4%',
              },
              legend: [{
                selectedMode: 'single',
                // data: categories.map(function (a) {
                //   return a.name;
                // })
              }],
              animationDuration: 3000,
              coordinateSystem: 'none',
              hoverAnimation: 1,
              // legend: [{
              //   data: ["类目0", "类目1", "类目2", "类目3", "类目4", "类目5", "类目6", "类目7", "类目8"]
              // }],
              // animationEasingUpdate: 'quinticInOut',
              // categories: [{
              //   name: "类目0"
              // }, {
              //   name: "类目1"
              // }, {
              //   name: "类目2"
              // }, {
              //   name: "类目3"
              // }, {
              //   name: "类目4"
              // }, {
              //   name: "类目5"
              // }, {
              //   name: "类目6"
              // }, {
              //   name: "类目7"
              // }, {
              //   name: "类目8"
              // }],
              series: [
                {
                  zoom: 0.6,  // 缩放比例
                  type: "graph",
                  layout: "circular",    // "force"
                  name: "source or sink",

                  circular: {
                    rotateLabel: true
                  },
                  symbolSize: 30,  //  节点大小
                  // edgeSymbol: ['circle', 'arrow'],
                  animation: true,
                  data: _this.data2,
                  edges: _this.edges2,

                  // 效果不明
                  // force: {
                  //   // repulsion: 200,
                  //   edgeLength: 300,
                  //   repulsion: 4,
                  //   gravity: 19,
                  //   layoutAnimation: true,
                  //   friction: 100
                  // },
                  edgeSymbolSize: 120,


                  focusNodeAdjacency: 1,
                  itemStyle: {// 点周围的阴影
                    borderColor: '#ffff',
                    borderWidth: 1,
                    shadowBlur: 10,
                    shadowColor: 'rgba(0, 0, 0, 0.6)'
                  },
                  roam: true,
                  label: {
                    position: 'right',
                    formatter: '{b}',
                    fontStyle: "oblique",
                    fontWeight: "bolder",
                    fontFamily: "Segoe Print",
                    color: "rgba(50, 15, 15, 1)",
                    fontSize: 20 // 标签的字体大小
                  },
                  lineStyle: {
                    color: "rgba(205, 130, 130, 30)",
                    curveness: 0.4,
                    width: 4,
                    type: "solid",
                    shadowBlur: 1
                  },
                  emphasis: {
                    lineStyle: {
                      width: 10
                    }
                  }
                },
              ],
            };
            // _this.data2.symbolSize=50;
            var theTopoChart = echarts.init(document.getElementById('tpc'));
            theTopoChart.setOption(optionOfTopo, true);
            // console.log(_this.edges2);
            // console.log(_this.data2);
          })
          .catch((error) => {
            console.log(error);
            alert('bad');
          });
      },

      getTableData(){// 未实现
        const _this = this
        this.$axios
          .get(`${window.$config.HOST}/api/n2n/list`,{
            params:{
              "role": ENUM('supernode', 'source-edge', 'sink-edge', 'hub-edge', 'web-edge', 'all' ) // 必需
            }
          })
          .then((response) => {
              _this.tableData=response.data.data;
              console.log(_this.tableData);
              alert('goodTableData')
          })
          .catch((error) => {
            console.log(error);
            alert('bad-table-data');
          });
      }
    },

    mounted() {
      this.getTopoData()
    }
  };
</script>

<style lang="less" scoped>
  .quick-container {
    .quick-card {
      height: 80vh;

      .echarts {
        width: 100%;
        height: 750px;
      }

      .el-card__header {
        padding: 0 20px;
        height: 48px;
        line-height: 48px;
      }

      .el-card__body {
        height: 100%;
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