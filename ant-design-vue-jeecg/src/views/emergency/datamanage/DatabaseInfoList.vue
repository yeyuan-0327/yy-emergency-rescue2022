<template>
  <a-card :bordered="false">
    <!-- 查询区域 -->
    <div class="table-page-search-wrapper">
      <a-form layout="inline" @keyup.enter.native="searchQuery">
        <a-row :gutter="24">
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <a-form-item label="表名">
              <a-input placeholder="请输入表名" v-model="queryParam.name"></a-input>
            </a-form-item>
          </a-col>
          <a-col :xl="6" :lg="7" :md="8" :sm="24">
            <span style="float: left;overflow: hidden;" class="table-page-search-submitButtons">
              <a-button type="primary" @click="searchQuery" icon="search">查询</a-button>
              <a-button type="primary" @click="searchReset" icon="reload" style="margin-left: 8px">重置</a-button>
<!--              <a @click="handleToggleSearch" style="margin-left: 8px">-->
<!--                {{ toggleSearchStatus ? '收起' : '展开' }}-->
<!--                <a-icon :type="toggleSearchStatus ? 'up' : 'down'"/>-->
<!--              </a>-->
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
<!--      <a-upload name="file" :showUploadList="false" :multiple="false" :headers="tokenHeader" :action="importExcelUrl" @change="handleImportExcel">-->
<!--        <a-button type="primary" icon="import">导入</a-button>-->
<!--      </a-upload>-->
      <!-- 高级查询区域 -->
<!--      <j-super-query :fieldList="superFieldList" ref="superQueryModal" @handleSuperQuery="handleSuperQuery"></j-super-query>-->
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

        <template slot="htmlSlot" slot-scope="text">
          <div v-html="text"></div>
        </template>
        <template slot="imgSlot" slot-scope="text">
          <span v-if="!text" style="font-size: 12px;font-style: italic;">无图片</span>
          <img v-else :src="getImgView(text)" height="25px" alt="" style="max-width:80px;font-size: 12px;font-style: italic;"/>
        </template>
        <template slot="fileSlot" slot-scope="text">
          <span v-if="!text" style="font-size: 12px;font-style: italic;">无文件</span>
          <a-button
            v-else
            :ghost="true"
            type="primary"
            icon="download"
            size="small"
            @click="downloadFile(text)">
            下载
          </a-button>
        </template>

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
             :title="showDatabaseVisibleTitle"
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
        <div>
          <a-select v-model="defaultOptions"
                    :options = "columnOptions"
                    style="width: 120px"
                    size="small"
                    @select="columnChange">
          </a-select>
        </div>
        <a-row :gutter="16">
          <a-col :span="12">
            <a-card :bordered="false" style="height: 250px">
              <div id="myChart" style="width: 650px; height: 270px">
              </div>
            </a-card>
          </a-col>
          <a-col :span="12">
            <a-card :bordered="true" style="height: 250px">
            </a-card>
          </a-col>
        </a-row>
        <br/>
        <a-row>
          <a-col :span="24">
            <a-card :bordered="true" style="height: 250px">
            </a-card>
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
  import {getAction, postAction} from "@/api/manage";
  import _ from 'lodash'

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
        showDatabaseVisibleTitle: '标题',
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
        //选中的单一数据库详细信息图
        // chart名称
        fieldChart:null,
        // 字段选择框
        columnOptions:[],
        defaultOptions : "",
        // 数据库列表
        columns: [
          {
            title: '序号',
            dataIndex: '',
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
      //chart初始化数据
      drawChart(field){
        // fieldChart实现
        let apiUrl = dataManageApi.apiSelectCharGroupByField;
        let fieldName = [field];
        postAction(apiUrl,fieldName).then((res)=>{
          if (res.success){
            let xData = []
            let yData = []
            // 遍历api返回数组
            _(res.result).forEach(function(i) {
              xData.push(i[field]);
              yData.push(i['num']);
            });
            // 正式画图
            const chartOption = {
              tooltip: {},
              xAxis: {
                data: xData
              },
              yAxis: {},
              series: [{
                name: '统计次数',
                type: 'bar',
                data: yData
              }]
            };
            if (this.fieldChart === null) this.fieldChart = this.$echarts.init(document.getElementById('myChart'))
            else this.fieldChart.clear()
            this.fieldChart.setOption(chartOption);
          }
        })

        //
      },
      //详情事件
      clickDatabaseToShow(record){
        this.showDatabaseVisible = true;
        this.showDatabaseVisibleTitle = record.name;
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
        // 初始化图表 传入默认第一个字段
        this.drawChart(this.defaultOptions);
      },
      // 改变字段后展示数据图
      columnChange(value) {
        this.drawChart(value);
      },
    }
  }
</script>
<style scoped>
  @import '~@assets/less/common.less';
</style>