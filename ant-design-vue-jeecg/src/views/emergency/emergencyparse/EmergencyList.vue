<template>
  <a-card :bordered="false" style="min-height: 650px">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchAllQuery">
        <a-row :gutter="24">
          <a-col :xl="7" :lg="7" :md="8" :sm="24">
            <a-form-item label="险情名称">
              <a-input placeholder="请输入险情名称" v-model="searchEmergencyName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="7" :lg="7" :md="8" :sm="24">
            <a-form-item label="任务名称">
              <a-input placeholder="请输入任务名称" v-model="searchTaskName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchAllQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchAllReset" icon="reload" style="margin-left: 8px">重置</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>
    <!-- 查询区域-END -->
    <a-row>
        <a-col :span="10" >
          <a-table :columns="columns"
                   :data-source="data"
                   :pagination="false"
                   :scroll="{ y:500 }"
          >
            <a slot="name" slot-scope="text" @click="nameClick(text)">{{ text }}</a>
            <span slot="customTitle"><a-icon type="smile-o" /> Name</span>
            <span slot="tags" slot-scope="tags">
          <a-tag
            v-for="tag in tags"
            :key="tag"
            :color="tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'"
          >
            {{ tag.toUpperCase() }}
          </a-tag>
          </span>
          </a-table>
        </a-col>
        <a-col :span="14">
          <div style="margin-left: 20px">
            <div>
              <a-table :columns="columns"
                       :data-source="data"
                       :pagination="false"
                       :scroll="{ y:200 }"
              >
                <a slot="name" slot-scope="text" @click="nameClick(text)">{{ text }}</a>
                <span slot="customTitle"><a-icon type="smile-o" /> Name</span>
                <span slot="tags" slot-scope="tags">
          <a-tag
            v-for="tag in tags"
            :key="tag"
            :color="tag === 'loser' ? 'volcano' : tag.length > 5 ? 'geekblue' : 'green'"
          >
            {{ tag.toUpperCase() }}
          </a-tag>
          </span>
              </a-table>
            </div>
            <br>
            <div>
              <a-descriptions bordered>
                <a-descriptions-item label="Product">
                  Cloud Database
                </a-descriptions-item>
                <a-descriptions-item label="Billing Mode">
                  Prepaid
                </a-descriptions-item>
                <a-descriptions-item label="Automatic Renewal">
                  YES
                </a-descriptions-item>
                <a-descriptions-item label="Order time">
                  2018-04-24 18:00:00
                </a-descriptions-item>
                <a-descriptions-item label="Usage Time" :span="2">
                  2019-04-24 18:00:00
                </a-descriptions-item>
                <a-descriptions-item label="Status" :span="3">
                  <a-badge status="processing" text="Running" />
                </a-descriptions-item>
                <a-descriptions-item label="Negotiated Amount">
                  $80.00
                </a-descriptions-item>
                <a-descriptions-item label="Discount">
                  $20.00
                </a-descriptions-item>
                <a-descriptions-item label="Official Receipts">
                  $60.00
                </a-descriptions-item>
              </a-descriptions>
            </div>
          </div>
        </a-col>
    </a-row>
  </a-card>
</template>

<script>
  const columns = [
    {
      dataIndex: 'name',
      key: 'name',
      slots: { title: 'customTitle' },
      // name handleClick
      scopedSlots: { customRender: 'name' },
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
    },
    {
      title: 'Address',
      dataIndex: 'address',
      key: 'address',
    },
    {
      title: 'Tags',
      key: 'tags',
      dataIndex: 'tags',
      scopedSlots: { customRender: 'tags' },
    },
  ];

  const data = [
    {
      key: '1',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
    {
      key: '4',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '5',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '6',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
    {
      key: '7',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '8',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '9',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
    {
      key: '2',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '3',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
    {
      key: '4',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '5',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '6',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },
    {
      key: '7',
      name: 'John Brown',
      age: 32,
      address: 'New York No. 1 Lake Park',
      tags: ['nice', 'developer'],
    },
    {
      key: '8',
      name: 'Jim Green',
      age: 42,
      address: 'London No. 1 Lake Park',
      tags: ['loser'],
    },
    {
      key: '9',
      name: 'Joe Black',
      age: 32,
      address: 'Sidney No. 1 Lake Park',
      tags: ['cool', 'teacher'],
    },

  ];
  export default {
    name: 'EmergencyList',
    data() {
      return {
        data,
        columns,
        searchEmergencyName:'',
        searchTaskName:'',

      };
    },
    methods: {
      //table name click
      nameClick(name){
        console.log(name)
      },
      //search button
      searchAllQuery(){

      },
      searchAllReset(){

      },
    },
  }
</script>

<style scoped>

</style>