<template>
  <a-card :bordered="false">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchQuery">
        <a-row :gutter="24">
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="表名">
              <a-input placeholder="请输入表名" v-model="queryParam.chineseName"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchReset" icon="reload" style="margin-left: 8px">重置</a-button>
            </span>
          </a-col>
        </a-row>
      </a-form>
    </div>
    <!-- 查询区域-END -->

    <!-- 操作按钮区域 -->
    <div class="table-operator">
      <a-button @click="handleAdd" type="primary" icon="plus">新增</a-button>
      <a-button type="primary" icon="download" @click="handleExportXls('基础数据库信息表')">导出</a-button>
      <a-dropdown v-if="selectedRowKeys.length > 0">
        <a-menu slot="overlay">
          <a-menu-item key="1" @click="batchDel"><a-icon type="delete"/>删除</a-menu-item>
        </a-menu>
        <a-button style="margin-left: 8px"> 批量操作 <a-icon type="down" /></a-button>
      </a-dropdown>
    </div>

    <!-- table区域-begin -->
    <div>
      <div class="ant-alert ant-alert-info" style="margin-bottom: 16px;">
        <i class="anticon anticon-info-circle ant-alert-icon"></i> 已选择 <a style="font-weight: 600">{{ selectedRowKeys.length }}</a>项
        <a style="margin-left: 24px" @click="onClearSelected">清空</a>
      </div>
      <a-table
        ref="table"
        size="middle"
        :scroll="{x:true}"
        bordered
        rowKey="id"
        :columns="columns"
        :dataSource="dataSource"
        :pagination="ipagination"
        :loading="loading"
        :rowSelection="{selectedRowKeys: selectedRowKeys, onChange: onSelectChange}"
        class="j-table-force-nowrap"
        @change="handleTableChange">

        <span slot="action" slot-scope="text, record">
          <a @click="handleEdit(record)">编辑</a>

          <a-divider type="vertical" />
          <a-dropdown>
            <a class="ant-dropdown-link">更多 <a-icon type="down" /></a>
            <a-menu slot="overlay">
              <a-menu-item>
                <a @click="clickDatabaseToShow(record)">详情</a>
              </a-menu-item>
              <a-menu-item>
                <a-popconfirm title="确定删除吗?" @confirm="() => handleDelete(record.id)">
                  <a>删除</a>
                </a-popconfirm>
              </a-menu-item>
            </a-menu>
          </a-dropdown>
        </span>

      </a-table>
    </div>
    <a-modal v-model="showDatabaseVisible"
             :title="showDatabaseVisibleChineseTitle"
             switchFullscreen
             :width="1400"
             :okButtonProps="{class:{'jee-hidden': true} }"
             cancelText="关闭">
      <div v-show="showType === 'table'">
        <a-table bordered
                 :scroll="{ y: 300 }"
                 :columns="showDatabaseTableColumns"
                 :dataSource="showDatabaseTableColumnsInfo"
                 :loading="showDatabaseTableLoading"
                 rowKey="ordinal_position" >
          <!--        :pagination="paginationDatabaseOpt"-->
        </a-table>
      </div>

      <div v-show="showType === 'chart'" >
        <a-row :gutter="16">
          <a-col :span="12">
            <div>
              <a-select v-model="defaultOptions"
                        :options = "columnOptions"
                        style="width: 120px"
                        size="small"
                        @select="columnChange">
              </a-select>
            </div>
              <div id="fieldChart" style="width: 100%; height: 400px">
              </div>
          </a-col>
          <a-col :span="12">
            <div>
              <a-select v-model="defaultOptionsSecond"
                        :options = "columnOptionsSecond"
                        style="width: 120px"
                        size="small"
                        @select="columnChangeSecond">
              </a-select>
            </div>
              <div id="sexChart" style="width: 600px; height: 400px">
              </div>
          </a-col>
        </a-row>
        <br/>
        <a-row>
          <a-col :span="24">
              <div id="birthChart" style="width: 100%; height: 300px">
              </div>
          </a-col>
        </a-row>
      </div>
      <br/>
      <a-radio-group v-model="showType">
        <a-radio-button value="table" @click="tableClick()">
          表
        </a-radio-button>
        <a-radio-button value="chart" @click="chartClick()">
          图
        </a-radio-button>
      </a-radio-group>

    </a-modal>
    <database-info-modal ref="modalForm" @ok="modalFormOk"></database-info-modal>
  </a-card>
</template>

<script>

  import '@/assets/less/TableExpand.less'
  import { mixinDevice } from '@/utils/mixin'
  import { JeecgListMixin } from '@/mixins/JeecgListMixin'
  import DatabaseInfoModal from './modules/DatabaseInfoModal'
  import ACol from 'ant-design-vue/es/grid/Col'
  import ARow from 'ant-design-vue/es/grid/Row'
  import { dataManageApi } from '@/api/EmergencyApi.js'
  import { postAction } from '@/api/manage'
  import _ from 'lodash'
  import * as echarts from 'echarts'

  export default {
    name: 'DatabaseInfoList',
    mixins:[JeecgListMixin, mixinDevice],
    components: {
      ARow,
      ACol,
      DatabaseInfoModal,
    },
    data () {
      return {
        description: '基础数据库信息表管理页面',
        //弹出框
        showDatabaseVisibleTitle: '',
        showDatabaseVisibleChineseTitle: '标题',
        showDatabaseVisible: false,
        showType: 'table',
        //选中的单一数据库详细信息表
        showDatabaseTableColumns:[
          {
            title: '序号',
            dataIndex: 'ordinal_position',
            width:80,
            align:"center",
          },
          {
            title:'字段英文名',
            align:"center",
            dataIndex: 'column_name'
          },
          {
            title:'字段中文名',
            align:"center",
            dataIndex: 'column_comment'
          },
          {
            title:'是否可为空',
            align:"center",
            dataIndex: 'is_nullable'
          },
          {
            title:'数据类型',
            align:"center",
            dataIndex: 'column_type'
          },
          {
            title:'数据键类型',
            align:"center",
            width:110,
            dataIndex: 'column_key'
          },
          {
            title:'有效数据量',
            align:"center",
            dataIndex: 'effective_data_volume'
          },
        ],
        showDatabaseTableColumnsInfo:[],
        showDatabaseTableLoading:false,
        //选中的单一数据库详细信息 图
        birthXField:[],
        fChart:null,
        bChart:null,
        // 字段选择框
        columnOptions:[],
        columnOptionsSecond:[],
        defaultOptions : "",
        defaultOptionsSecond:"",
        // 数据库列表
        columns: [
          {
            title: '序号',
            key:'rowIndex',
            width:60,
            align:"center",
            customRender:function (t,r,index) {
              return parseInt(index)+1;
            }
          },
          {
            title:'表名',
            align:"center",
            dataIndex: 'name'
          },
          {
            title:'中文名',
            align:"center",
            dataIndex: 'chineseName'
          },
          {
            title:'数据库类型',
            align:"center",
            dataIndex: 'databaseProject_dictText'
          },
          {
            title:'描述信息',
            align:"center",
            dataIndex: 'content'
          },
          {
            title:'创建日期',
            align:"center",
            dataIndex: 'createTime'
          },
          {
            title: '操作',
            dataIndex: 'action',
            align:"center",
            fixed:"right",
            width:147,
            scopedSlots: { customRender: 'action' }
          }
        ],
        url: {
          list: "/datamanage/databaseInfo/list",
          delete: "/datamanage/databaseInfo/delete",
          deleteBatch: "/datamanage/databaseInfo/deleteBatch",
          exportXlsUrl: "/datamanage/databaseInfo/exportXls",
          importExcelUrl: "datamanage/databaseInfo/importExcel",
        },
        dictOptions:{},
        superFieldList:[],
      }
    },
    created() {
      this.getSuperFieldList();
    },
    computed: {
      importExcelUrl: function(){
        return `${window._CONFIG['domianURL']}/${this.url.importExcelUrl}`;
      },
    },
    methods: {
      initDictConfig(){
      },
      getSuperFieldList(){
        let fieldList=[];
        fieldList.push({type:'string',value:'name',text:'表名',dictCode:''})
        fieldList.push({type:'string',value:'chineseName',text:'中文名',dictCode:''})
        fieldList.push({type:'string',value:'databaseProject',text:'数据库类型',dictCode:'database_project'})
        fieldList.push({type:'string',value:'content',text:'描述信息',dictCode:''})
        fieldList.push({type:'datetime',value:'createTime',text:'创建日期'})
        this.superFieldList = fieldList
      },
      //搜索按钮
      searchQuery(){
        if (this.dataSource && this.queryParam.chineseName !== '') {
          this.dataSource = this.dataSource.filter(
            (p) => p.chineseName.indexOf(this.queryParam.chineseName) !== -1
          )
        }
      },
      //chart初始化数据
      drawChart(field,fieldSecond){
        // 左上角图
        let apiUrl = dataManageApi.apiSelectCharGroupByField;
        let fieldTableList = [field,this.showDatabaseVisibleTitle];
        postAction(apiUrl,fieldTableList).then((res)=>{
          if (res.success){
            drawBarChart(res.result)
            function drawBarChart(_barData){
              let xData = []
              let yData = []
              // 遍历api返回数组
              _(_barData).forEach(function(i) {
                xData.push(i[field]);
                yData.push(i['num']);
              });
              // 画左上角图
              const fieldChartOption = {
                tooltip: {},
                xAxis: {
                  axisLabel:{
                    interval: 0,
                    rotate:25
                  },
                  data: xData
                },
                yAxis: {},
                series: [{
                  name: '统计次数',
                  type: 'bar',
                  data: yData
                }]
              };
              if (document.getElementById('fieldChart') != null) echarts.dispose(document.getElementById('fieldChart'))
              let fieldChart = echarts.init(document.getElementById('fieldChart'))
              fieldChart.setOption(fieldChartOption,true);
            }
          }
        })
        // 右上角图
        apiUrl = dataManageApi.selectCharGroupBySexField;
        fieldTableList = [field,this.showDatabaseVisibleTitle,fieldSecond]
        postAction(apiUrl,fieldTableList).then((res)=>{
          if (res.success){
            drawPie(_.last(res.result), _.initial(res.result))
            function drawPie(innerPieData,outPieData) {
              let innerData = []
              _.forEach(innerPieData,function(value,key) {
                innerData.push(
                  { value:value,name:key }
                )
              })
              let outData = []
              _.forEach(outPieData,function(value) {
                outData.push({
                  value:value['count'],
                  name:value[field]+value[fieldSecond]
                })
              })
              let sexOption = {
                tooltip: {
                },
                series: [
                  {
                    name: '数量',
                    type: 'pie',
                    center:'50%',
                    selectedMode: 'single',
                    radius: '30%',
                    label: {
                      position: 'inner',
                      fontSize: 14
                    },
                    labelLine: {
                    },
                    data: innerData
                  },
                  {
                    name: '统计数量',
                    type: 'pie',
                    center:'50%',
                    radius: ['50%', '65%'],
                    labelLine: {
                      length: 20
                    },
                    label: {
                      rich: {
                        a: {
                          color: '#6E7079',
                          lineHeight: 22,
                          align: 'center'
                        },
                        hr: {
                          borderColor: '#8C8D8E',
                          width: '100%',
                          borderWidth: 1,
                          height: 0
                        },
                        b: {
                          color: '#4C5058',
                          fontSize: 14,
                          fontWeight: 'bold',
                          lineHeight: 33
                        },
                        per: {
                          color: '#fff',
                          backgroundColor: '#4C5058',
                          padding: [3, 4],
                          borderRadius: 4
                        }
                      }
                    },
                    data: outData
                  }
                ]
              };
              if (document.getElementById('sexChart') != null)echarts.dispose(document.getElementById('sexChart'))
              let sexChart = echarts.init(document.getElementById('sexChart'))
              sexChart.setOption(sexOption);
            }
          }
        })

        // 正下方图
        apiUrl = dataManageApi.selectCharGroupByBirthField;
        fieldTableList = [field,this.showDatabaseVisibleTitle];
        postAction(apiUrl,fieldTableList).then((res)=>{
          if (res.success) {
            if (res.success) {
              let resData = res.result
              drawBirthLine(_.tail(resData))
              //画正下方图
              function drawBirthLine(_rawData) {
                const fields = resData[0];
                const datasetWithFilters = [];
                const seriesList = [];
                echarts.util.each(fields, function (field) {
                  const datasetId = 'dataset_' + field;
                  datasetWithFilters.push({
                    id: datasetId,
                    fromDatasetId: 'dataset_raw',
                    transform: {
                      type: 'filter',
                      config: {
                        and: [
                          { dimension: 'Year', gte: 1 },
                          { dimension: 'Field', '=': field }
                        ]
                      }
                    }
                  });
                  seriesList.push({
                    type: 'line',
                    datasetId: datasetId,
                    showSymbol: false,
                    name: field,
                    endLabel: {
                      show: true,
                      formatter: function (params) {
                        return params.value[1] + ': ' + params.value[0];
                      }
                    },
                    labelLayout: {
                      moveOverlap: 'shiftY'
                    },
                    emphasis: {
                      focus: 'series'
                    },
                    encode: {
                      x: 'Year',
                      y: 'Count',
                      label: ['Field', 'Count'],
                      itemName: 'Year',
                      tooltip: ['Count']
                    }
                  });
                });
                const birthChartOption = {
                  animationDuration: 10000,
                  dataset: [
                    {
                      id: 'dataset_raw',
                      source: _rawData
                    },
                    ...datasetWithFilters
                  ],
                  title: {
                    text: '随着年龄段变化趋势'
                  },
                  tooltip: {
                    order: 'valueDesc',
                    trigger: 'axis'
                  },
                  xAxis: {
                    type: 'category',
                    nameLocation: 'middle'
                  },
                  yAxis: {
                    name: '统计个数'
                  },
                  grid: {
                    right: 140
                  },
                  series: seriesList
                };
                if (document.getElementById('birthChart') != null) echarts.dispose(document.getElementById('birthChart'))
                let birthChart = echarts.init(document.getElementById('birthChart'))
                birthChart.setOption(birthChartOption,true);
              }
            }
          }
        })

      },
      //详情事件
      clickDatabaseToShow(record){
        this.showDatabaseVisible = true;
        this.showDatabaseVisibleTitle = record.name;
        this.showDatabaseVisibleChineseTitle = record.chineseName;
        let apiUrl = dataManageApi.apiClickDetailTable
        let tableName = [record.name];
        postAction(apiUrl,tableName).then((res)=>{
          if (res.success){
            this.showDatabaseTableColumnsInfo = res.result
          }
        })
      },
      //弹出框 表图切换按钮点击事件
      tableClick(){
      },
      chartClick(){
        // 初始化字段选择器
        const temp = []
        _(this.showDatabaseTableColumnsInfo).forEach(function(i) {
          let disableColumnOption = dataManageApi.disableColumnOption
          //黑名单判断
          if(disableColumnOption.indexOf(i['column_name']) === -1){
            temp.push({
              value: i['column_name'],
              label: i['column_comment']
            })
          }
        });
        this.defaultOptions = temp[0].value;
        this.columnOptions = temp;
        this.columnOptionsSecond = temp;
        this.defaultOptionsSecond = this.columnOptionsSecond[1].value
        // 初始化图表 传入默认第一个字段
        this.drawChart(this.defaultOptions,this.defaultOptionsSecond);
      },
      // 改变字段后展示数据图
      columnChange(value) {
        this.defaultOptions=value;
        this.drawChart(value,this.defaultOptionsSecond);
      },
      columnChangeSecond(value) {
        this.defaultOptionsSecond = value
        this.drawChart(this.defaultOptions,value);
      },
    }
  }
</script>
<style scoped>
  @import '~@assets/less/common.less';
</style>