<template>
<div class="container">
<el-card class="box-card">
  <div class="head">
    <h1 class="title" style="display:inline-block">私有仓库信息</h1>
    <el-tag class="info-tag" type="success" effect="dark">
      IP:192.168.1.1
    </el-tag>
    <el-tag class="info-tag" type="warning" effect="dark">
      PORT:8080
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
    <el-button type="primary" style="margin:10px;">新增</el-button>
    <el-table
    :data="tableData"
    style="width: 98%;margin-left:10px;"
    max-height="250">
    <el-table-column
      prop="name"
      label="名称"
      >
    </el-table-column>
    <el-table-column
      prop="status"
      label="状态"
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
          @click.native.prevent="deleteRow(scope.$index, tableData)"
          type="text"
          size="small">
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
methods: {
      deleteRow(index, rows) {
        rows.splice(index, 1);
      }
    },
    data() {
      return {
        tableData: [{
          name: '王小虎',
          status:'',
          vlan_ip: '普陀区',
          uncertain: '...',
        }]
      }
    }
}
</script>

<style scoped>
.box-card {
    width: 100%;
    margin:0 auto;
  }
.text {
    font-size: 14px;
  }

  .item {
    padding: 18px 0;
  }
  .title{
    font-size:24px;
    margin:10px;
  }
  .el-tag{
    height:35px;
    /* padding:10px; */
    line-height: 35px;
    font-size:18px;
    margin-right:10px;
  }
  .info-button{
    float:right;
    margin:20px;
  }
  
</style>