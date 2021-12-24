<template>
  <a-card :bordered="false">
    <a-modal v-model="dwRelationshipModal"
             :title="dwRelationshipModalChineseTitle"
             switchFullscreen
             :width="1400"
             :okButtonProps="{class:{'jee-hidden': true} }"
             cancelText="关闭">

      <div v-show="showType === 'table'" >
      <a-table bordered
               :scroll="{ x:2000 , y: 400 }"
               :columns="factTableColumns"
               :dataSource="factTableData"
               :loading="factTableLoading"
               rowKey="item_id"
               :pagination="paginationOpt">
      </a-table>
      </div>
      <div v-show="showType === 'chart'" >
        <a-row :gutter="16">
          <a-col :span="12">
            <div>
              <a-select v-model="defaultFieldOptions"
                        :options = "fieldOptions"
                        style="width: 120px"
                        size="small"
                        @select="columnChangeSelect">
              </a-select>
            </div>
            <div id="factChart" style="width: 1300px; height: 500px">
            </div>
          </a-col>
        </a-row>
      </div>

      <a-radio-group v-model="showType">
        <a-radio-button value="chart" @click="chartClick()">
          数据说明图
        </a-radio-button>
      </a-radio-group>

    </a-modal>
    <div id="myChart" style="width: 100%; height: 1000px">
    </div>
  </a-card>
</template>

<script>
  import {getAction, postAction} from "@/api/manage";
  import * as echarts from 'echarts';
  import { dataManageApi } from '@/api/EmergencyApi.js'
  import _ from 'lodash'

  export default {
    name: 'DwRelationChart',
    data(){
      return{
        dwRelationshipModalChineseTitle:'',
        dwRelationshipModal:false,
        // 表
        factTableColumns:[],
        factTableData: [],
        factTableLoading:false,
        factTable: '',
        showType: "table",
        // 字段选择框
        defaultFieldOptions:"",
        fieldOptions:[],
        //数据分页设置
        paginationOpt: {
          defaultCurrent: 1, // 默认当前页数
          defaultPageSize: 20, // 默认当前页显示数据的大小
          total: 0, // 总数，必须先有
          showSizeChanger: true,
          showQuickJumper: true,
          pageSizeOptions: ["5", "10", "15", "20"],
          showTotal: (total) => `共 ${total} 条`, // 显示总数
          onShowSizeChange: (current, pageSize) => {
            this.paginationOpt.defaultCurrent = 1;
            this.paginationOpt.defaultPageSize = pageSize;
          },
          // 改变每页数量时更新显示
          onChange: (current, size) => {
            this.paginationOpt.defaultCurrent = current;
            this.paginationOpt.defaultPageSize = size;
          },
        },
      }
    },
    mounted() {
      this.drawEcharts();
    },
    methods:{
      drawEcharts(){
        let apiUrl = dataManageApi.fetchDimFactRelation
        getAction(apiUrl).then((res)=>{
          if (res.success){
            drawRelationChart(res.result)
            let that = this
            function drawRelationChart(data) {
              let dataPoint = []
              let dataLink = []
              _.forEach(data,function(value) {
                if (value['type']==='fact'){
                  dataPoint.push({
                    name: value['name'],
                    value: value['value'],
                    des: value['des'],
                    type:value['type'],
                    symbolSize: 150,
                    itemStyle: {
                      normal: {
                        color: 'red'
                      }
                    }
                  })
                }
                else if(value['type']==='dim'){
                  dataPoint.push({
                    name: value['name'],
                    value: value['value'],
                    type:value['type'],
                    des: value['des'],
                    symbolSize: 100,
                  })
                }
                else {
                  dataLink.push({
                    source: value['source'],
                    target: value['target'],
                    type:value['type'],
                    name: '',
                    des: '',
                    lineStyle: {
                      normal: {
                        color: '#000',
                      }
                    }
                  })
                }
              })
              let option = {
                title: { text: '数据仓库关系图谱',textStyle:{
                  fontSize:20
                  }
                },
                tooltip: {
                  formatter: function (x) {
                    return x.data.des;
                  }
                },
                series: [
                  {
                    type: 'graph',
                    layout: 'force',
                    symbolSize: 80,
                    roam: true,
                    edgeSymbol: ['circle', 'arrow'],
                    edgeSymbolSize: [4, 10],
                    draggable: true,
                    itemStyle: {
                      normal: {
                        color: '#4b565b'
                      }
                    },
                    lineStyle: {
                      normal: {
                        width: 2,
                        color: '#4b565b'
                      }
                    },
                    edgeLabel: {
                      normal: {
                        show: true,
                        formatter: function (x) {
                          return x.data.name;
                        }
                      }
                    },
                    label: {
                      normal: {
                        show: true,
                        fontSize:12
                      }
                    },
                    force:{
                      repulsion:2000,
                      edgeLength:250
                    },
                    data: dataPoint,
                    links: dataLink
                  }
                ]
              };
              let myChart = echarts.init(document.getElementById('myChart'))
              myChart.setOption(option);
              myChart.on('click',function(params) {
                if (params.data.type==='fact') that.dwModal(params.data)
              })
            }
          }
        })
      },
      dwModal(data){
        this.showType = "table"
        this.dwRelationshipModal = true
        this.dwRelationshipModalChineseTitle = data.name;
        let tableName = data.value
        this.factTable = tableName
        let postList = [tableName]
        let apiUrl = dataManageApi.fetchDwData
        postAction(apiUrl,postList).then((res)=>{
          if (res.success){
            let temp_column = []
            temp_column.push({
              title: '序号',
              dataIndex: 'rowIndex',
              width:60,
              align:"center",
              customRender: (text, record, index) =>
                `${(this.paginationOpt.defaultCurrent - 1) *
                this.paginationOpt.defaultPageSize +
                index + 1}`
            })
            let data = res.result
            _.forEach(_.head(data),function(value) {
              temp_column.push({
                title:value.title,
                align:"center",
                dataIndex: value.dataIndex,
                key: value.dataIndex,
              })
            })
            this.factTableColumns = temp_column
            let table_data = _.tail(data)
            let temp_data = []
            let count = 1;
            _.forEach(table_data[0],function(value) {
              value['item_id']= count
              _.forEach(value,function(i,j) {value[j]=String(i);})
              temp_data.push(value)
              count ++;
            })
            this.factTableData = temp_data
          }
        })
      },
      chartClick(){
        // 初始化字段选择器
        let temp = []
        _(this.factTableColumns).forEach(function(i) {
          let disableColumnOption = dataManageApi.disableColumnOption
          //黑名单判断
          if(disableColumnOption.indexOf(i['key']) === -1){
            temp.push({
              value: i['key'],
              label: i['title']
            })
          }
        });
        temp = _.tail(temp)
        this.defaultFieldOptions = temp[0].value;
        this.fieldOptions = temp;
        this.drawFactChart(this.defaultFieldOptions)
      },
      columnChangeSelect(value){
        this.drawFactChart(value)
      },
      drawFactChart(field){
        if (document.getElementById('factChart') != null) echarts.dispose(document.getElementById('factChart'))
        let factChart = echarts.init(document.getElementById('factChart'));
        factChart.showLoading();
        let apiUrl = dataManageApi.factDataTable
        let postList = [field,this.factTable]
        postAction(apiUrl,postList).then((res)=>{
          if (res.success){
            drawBarChart(res.result)
            function drawBarChart(_barData) {
              let xData = []
              let yData = []
              // 遍历api返回数组
              _(_barData).forEach(function(i) {
                xData.push(i[field]);
                yData.push(i['count']);
              });
              // 指定图表的配置项和数据
              let option = {
                tooltip: {},
                yAxis: {
                  axisLabel:{
                    interval: 0,
                    rotate:25
                  },
                  data: xData
                },
                xAxis: {
                },
                series: [
                  {
                    data: yData,
                    type: 'bar'
                  }
                ]
              }
              // 使用刚指定的配置项和数据显示图表。
              factChart.hideLoading();
              factChart.setOption(option,true);
            }
          }
        })
      }
    },
  }
</script>

<style scoped>
  #components-popover-demo-placement .ant-btn {
    width: 70px;
    text-align: center;
    padding: 0;
    margin-right: 8px;
    margin-bottom: 8px;
  }
</style>