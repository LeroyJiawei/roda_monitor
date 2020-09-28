<template>
  <div class="container">
    <el-card class="box-card">
      <div class="head">
        <h1 class="title" style="display: inline-block">私有仓库信息</h1>
        <el-tag class="info-tag" type="success" effect="dark">
          IP:{{ hub_info.addr }}
        </el-tag>
        <el-tag class="info-tag" type="warning" effect="dark">
          PORT:{{ hub_info.port }}
        </el-tag>
      </div>
    </el-card>

    <div class="info-button">
      <el-button type="primary">新增</el-button>
      <el-button type="warning">修改</el-button>
      <el-button type="danger">删除</el-button>
    </div>
    <el-card class="box-card">
      <div class="image-manager">
        <h1 class="title">Image管理</h1>
        <el-button type="primary" style="margin: 10px">新增</el-button>
        <el-table
          :data="tableData"
          style="width: 98%; margin-left: 10px"
          max-height="250"
        >
          <el-table-column prop="name" label="名称"> </el-table-column>
          <el-table-column prop="tag" label="标签"> </el-table-column>
          <el-table-column prop="status" label="状态"> </el-table-column>
          <el-table-column prop="vlan_ip" label="vlan IP"> </el-table-column>

          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button
                @click.native.prevent="deleteRow(scope.$index, tableData)"
                type="text"
                size="small"
              >
                移除
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      hub_info: {
        addr: "1.2.3.4",
        port: "8081",
      },
      tableData: [
        {
          name: "王小虎",
          tag: ["1", "2"],
          status: "close",
          vlan_ip: "普陀区",
        },
        {
          name: "王大虎",
          tag: ["3", "4"],
          status: "open",
          vlan_ip: "闵行区",
        },
      ],
    };
  },
  methods: {
    async getHubInfoAndImages() {
      await this.$axios
        .get(`${window.$config.HOST}/api/hub/info`)
        .then((response) => {
          if (response.data.status != "OK") {
            alert("Hub信息获取失败！");
            console.log(response.data);
          } else this.hub_info = response.data.data;
        })
        .catch((error) => {
          console.log(error);
          alert("Hub信息获取失败,通信错误");
        });

      await this.$axios
        .get(`${window.$config.HOST}/api/hub/list_images`)
        .then((response) => {
          if (response.data.status != "OK") {
            alert("Images信息获取失败！");
            console.log(response);
          } else this.tableData = response.data.data;
        })
        .catch((error) => {
          console.log(error);
          alert("Images信息获取失败,通信错误");
        });
    },
    deleteRow(index, rows) {
      // rows.splice(index, 1);
      console.log(this.tableData[index]);
      this.$axios({
        url: `${window.$config.HOST}/api/hub/delete_image`,
        method: "delete",
        data: {
          name: this.tableData[index].name,
          tag: this.tableData[index].tags[0],
        }, // body参数
      })
        .then((response) => {
          // console.log(response);
          if (response.data.status == "OK") {
            alert("删除成功！");
          } else {
            alert("image删除失败!");
            console.log(response);
          }
        })
        .catch((error) => {
          alert("image删除失败，前后端通信错误");
          console.log(error);
        });
    },
  },
  mounted() {
    this.getHubInfoAndImages();
  },
};
</script>

<style scoped>
.box-card {
  width: 100%;
  margin: 0 auto;
}

.text {
  font-size: 14px;
}

.item {
  padding: 18px 0;
}

.title {
  font-size: 24px;
  margin: 10px;
}

.el-tag {
  height: 35px;
  /* padding:10px; */
  line-height: 35px;
  font-size: 18px;
  margin-right: 10px;
}

.info-button {
  float: right;
  margin: 20px;
}
</style>