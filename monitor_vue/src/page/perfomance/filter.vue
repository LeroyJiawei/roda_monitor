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
          <el-table-column prop="filter_exist" label="是否部署">
          </el-table-column>
          <el-table-column prop="filter_base_rate" label="baserate">
          </el-table-column>
          <el-table-column prop="filter_win_size" label="窗口大小">
          </el-table-column>
          <el-table-column prop="filter_exp_match" label="匹配阈值">
          </el-table-column>
          <el-table-column prop="filter_max_thread" label="最大线程数">
          </el-table-column>
          <el-table-column prop="state" label="状态"> </el-table-column>

          <el-table-column label="操作" fixed="right">
            <template slot-scope="scope">
              <span>
                <el-button
                  style="display: block; margin: 0 auto; height: 35px"
                  @click="filterDialClick(scope.$index)"
                  type="text"
                  size="small"
                >
                  修改filter配置
                </el-button>
              </span>

              <!-- <span>
                <el-button
                  style="display: block; margin: 0 auto; height: 35px"
                  @click="deleteRow(scope.$index)"
                  type="danger"
                  size="small"
                >
                  删除
                </el-button>
              </span> -->
            </template>
          </el-table-column>
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

    <el-dialog
      title="filter配置"
      :visible.sync="FilterPageVisible"
      width="50%"
      :before-close="handleFilterDialClose"
      :modal-append-to-body="false"
    >
      <el-form
        :model="filterDialData"
        status-icon
        ref="filterDialData"
        label-width="130px"
        :rules="rulesOfConfigNode"
      >
        <el-form-item label="名称" prop="name">
          <el-input
            type="text"
            v-model="filterDialData.name"
            :disabled="true"
          ></el-input>
        </el-form-item>

        <el-form-item label="baserate" prop="baserate">
          <el-input
            type="text"
            v-model.number="filterDialData.baserate"
          ></el-input>
        </el-form-item>

        <el-form-item label="窗口大小" prop="winSize">
          <el-input
            type="text"
            v-model.number="filterDialData.winSize"
          ></el-input>
        </el-form-item>

        <el-form-item label="匹配阈值" prop="expMatchTime">
          <el-input
            type="text"
            v-model.number="filterDialData.expMatchTime"
          ></el-input>
        </el-form-item>

        <el-form-item label="最大线程数" prop="maxThreads">
          <el-input
            type="text"
            v-model.number="filterDialData.maxThreads"
          ></el-input>
        </el-form-item>
      </el-form>

      <span slot="footer" class="dialog-footer">
        <el-button
          @click="
            FilterPageVisible = false;
            resetNodeForm('filterDialData');
          "
          >取 消</el-button
        >

        <el-button type="danger" @click="deleteFilter('filterDialData')">
          删除filter
        </el-button>

        <el-button
          type="primary"
          @click="submitFilterModification('filterDialData')"
          >提交修改</el-button
        >
      </span>
    </el-dialog>
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
      FilterPageVisible: false,
      filterDialData: {},

      filterRadio: null,
      filterList: [],
      filterChoose: [],

      rulesOfConfigNode: {
        baserate: [
          { required: true, message: "不能为空" },
          { type: "float", message: "范围：0～1" },
        ],
        winSize: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" },
        ],
        expMatchTime: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" },
        ],
        maxThreads: [
          { required: true, message: "不能为空" },
          { type: "number", message: "必须为数字值" },
        ],
      },

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
    this.loadFilterInfo();
  },
  mounted() {
    const that = this;

    that.intervalId = setInterval(function () {
      if (
        that.filterChoose.length >= 1 &&
        that.filterChoose[0].filter_exist == "Yes"
      ) {
        that.$axios
          .get(`${window.$config.HOST}/api/filter/match_perf`, {
            params: {
              filter_id: that.filterChoose[0].id,
              addr: that.filterChoose[0].addr,
              influx_port: that.filterChoose[0].influx_port,
            },
          })
          .then((response) => {
            if (response.data.status == "OK") {
              var getData = response.data.data;
              if (chart1_data.length == 20) {
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
            }
          })
          .catch((error) => {
            console.log(error);
          });
      }
      // else {
      //   if (chart1_data.length == 20) {
      //     chart1_data.shift();
      //     chart2_data.shift();
      //     chart3_data.shift();
      //     chart4_data.shift();
      //   }
      //   var cur_date = new Date();
      //   var date_val =
      //     [
      //       cur_date.getFullYear(),
      //       cur_date.getMonth(),
      //       cur_date.getDate(),
      //     ].join("/") +
      //     " " +
      //     [
      //       cur_date.getHours(),
      //       cur_date.getMinutes(),
      //       cur_date.getSeconds(),
      //     ].join(":");
      //   chart1_data.push({
      //     name: cur_date.toString(),
      //     value: [date_val, 0],
      //   });
      //   chart2_data.push({
      //     name: cur_date.toString(),
      //     value: [date_val, 0],
      //   });
      //   chart3_data.push({
      //     name: cur_date.toString(),
      //     value: [date_val, 0],
      //   });
      //   chart4_data.push({
      //     name: cur_date.toString(),
      //     value: [date_val, 0],
      //   });
      // }
    }, 1000);
  },
  methods: {
    loadFilterInfo() {
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
    radioChange(val) {
      this.filterList.forEach((ele) => {
        if (ele.name === val) {
          this.filterChoose = [ele];
        }
      });
      // chart1_data = [];
    },

    filterDialClick(index) {
      this.filterDialData.id = this.filterList[index].id;
      this.filterDialData.network_id = this.filterList[index].network_id;
      this.filterDialData.name = this.filterList[index].name;

      this.filterDialData.influx_port = this.filterList[index].influx_port;

      this.filterDialData.baserate = this.filterList[index].filter_base_rate;
      this.filterDialData.expMatchTime = this.filterList[
        index
      ].filter_exp_match;
      this.filterDialData.maxThreads = this.filterList[index].filter_max_thread;
      this.filterDialData.winSize = this.filterList[index].filter_win_size;

      this.FilterPageVisible = true;
    },

    handleFilterDialClose(done) {
      this.filterDialData = {};
      this.FilterPageVisible = false;
    },

    // 新增节点相关函数：
    resetNodeForm(formName) {
      //  重置，点击取消按钮后清空输入的节点信息
      this.$refs[formName].resetFields();
    },

    deleteFilter(formName) {
      this.$axios({
        url: `${window.$config.HOST}/api/filter/delete`,
        method: "delete",
        data: {
          id: this.filterDialData.id,
        },
      })
        .then((response) => {
          if (response.data.status == "OK") {
            this.$message({ message: "删除成功！" });
            this.FilterPageVisible = false;
            this.filterDialData = {};
            this.loadFilterInfo();
          } else {
            this.$message.error({ message: "删除失败!" });
            console.log(response);
          }
        })
        .catch((error) => {
          console.log(error);
          this.$message.error({ message: "删除失败，前后端通信错误!" });
        });
    },

    submitFilterModification(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.$axios
            .post(`${window.$config.HOST}/api/filter/update_config`, {
              id: this.filterDialData.id,
              network_id: this.filterDialData.network_id,
              win_size: this.filterDialData.winSize,
              match_threshold: this.filterDialData.expMatchTime,
              base_rate: this.filterDialData.baserate,
              max_thread: this.filterDialData.maxThreads,
              influx_port: this.filterDialData.influx_port,
            })
            .then((response) => {
              if (response.data.status == "OK") {
                this.$message({ message: "修改成功！" });

                this.FilterPageVisible = false;
                this.modifyNodeData = {};
                this.loadFilterInfo();
              } else {
                this.$message.error({ message: "修改失败！" });

                console.log(response);
              }
            })
            .catch((error) => {
              console.log(error);
              this.$message.error({ message: "修改失败，前后端通信错误!" });
            });
        } else {
          this.$message.error({ message: "请填写相关内容" });

          return false;
        }
      });
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