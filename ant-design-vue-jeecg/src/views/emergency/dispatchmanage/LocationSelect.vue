<template>
  <a-card>
    <a-row>
<!--  折叠面板-->
      <a-col :span="11">
        <a-collapse v-model="activeKey" expand-icon-position="right" @change="paddleChange" accordion>
          <a-collapse-panel v-for="item in paddleData" :key="String(item.id)" :header="item.name" >
            <div>
              <a-table :columns="columns"
                       :data-source="item.taskData"
                       :pagination="false"
                       style="margin-left: -8px"
                       size="middle" >
              <span slot="action" slot-scope="text, record">
                  <a @click="handleTaskEdit(record)">更改</a>
                  <a-divider type="vertical" />
                  <a @click="handleTaskAddressShow(record)">查看</a>
              </span>
              </a-table>
            </div>
            <a-dropdown slot="extra" :trigger="['click']">
              <a class="ant-dropdown-link" @click="handleClickSetting" style="color: inherit;">
                <a-icon type="setting" />
              </a>
              <a-menu slot="overlay">
                <a-menu-item key="0" @click="emergencyAddressChange(item)">
                  险情地址更改
                </a-menu-item>
                <a-menu-item key="1" @click="">
                  险情负责人选取
                </a-menu-item>
              </a-menu>
            </a-dropdown>
          </a-collapse-panel>
        </a-collapse>
      </a-col>
<!--   地图模块-->
      <a-col :span="13">
        <a-spin :spinning="mapSpinning">
          <a-icon slot="indicator" type="loading" style="font-size: 100px" spin />
          <div id="map-container"></div>
          <br>
          <div>
            <div>
              <a-space :size="20">
                <span class="input-item-text">经纬度</span>
                <a-input :value='lngLat' type="text" style="width: 200px" disabled ></a-input>
                <span class="input-item-text" >地址</span>
                <a-input :value="address" type="text" style="width: 300px" disabled></a-input>
                <a-button type="primary" @click="lngLatConfirm" :disabled="!clickMapPoint">确认</a-button>
              </a-space>
            </div>
          </div>
        </a-spin>
      </a-col>
    </a-row>
  </a-card>
</template>

<script>
  import AMapLoader from '@amap/amap-jsapi-loader'
  import {getAction, postAction,uploadAction} from "@/api/manage";
  import { dispatchManage } from '@/api/EmergencyApi.js'

  window._AMapSecurityConfig = {
    securityJsCode: '85d1a2595ee470f1444abba517987f62',
  }

  const columns = [
    {
      title: '任务名称',
      dataIndex: 'name',
    },
    {
      title: '险情地址',
      dataIndex: 'address',
    },
    {
      title: '任务地址(默认)',
      dataIndex: 'taskAddress',
    },
    {
      title: '操作',
      key: 'action',
      scopedSlots: { customRender: 'action' },
    },
  ];
  const data = [
    {
      key: '0',
      name: '社会动员',
      taskAddress: '经开区丰报云村',
      address: '经开区丰报云村',
      lngLat:'',
    },
    {
      key: '1',
      name: '治安维护',
      taskAddress: '经开区丰报云村',
      address: '经开区丰报云村',
      lngLat:'',
    },
    {
      key: '2',
      name: '医疗救护',
      taskAddress: '经开区丰报云村',
      address: '经开区丰报云村',
      lngLat:'',
    },
  ];
  export default {
    name: 'LocationSelect',
    data(){
      return{
        activeKey: [],
        address:'',
        lngLat:'',
        // 折叠面板数据
        paddleData:[],
        columns,
        // map load
        mapSpinning:true,
        // 允许地图点击
        clickMapPoint:false,
        // map
        map:undefined,
        marker:undefined,
        clickTaskChangeId:undefined,
      }
    },
    // watch: {
    //   activeKey(key) {
    //     console.log(key);
    //   },
    // },
    beforeCreate() {
      AMapLoader.load({
        "key": "a9f0503b06980a2144a8660a86f74492",              // 申请好的Web端开发者Key，首次调用 load 时必填
        "version": "1.4.15",    // 指定要加载的 JSAPI 的版本，缺省时默认为 1.4.15
        "plugins": [],          // 需要使用的的插件列表，如比例尺'AMap.Scale'等
        "AMapUI": {             // 是否加载 AMapUI，缺省不加载
          "version": '1.1',   // AMapUI 缺省 1.1
          "plugins":[]        // 需要加载的 AMapUI ui插件
        },
        "Loca": {               // 是否加载 Loca， 缺省不加载
          "version": '1.3.2'  // Loca 版本，缺省 1.3.2
        }
      }).then( AMap => {
        this.$nextTick(() => this.initMap(AMap));
        this.mapSpinning = false
      }).catch(e => {
        console.error(e);
      })
    },
    created(){
      this.initEmergencies()
    },
    methods: {
      //加载险情
      initEmergencies(){
        let apiUrl = dispatchManage.getEmergencies
        getAction(apiUrl).then((res)=>{
          if (res.success){
            this.paddleData=res.result
            // 默认打开第一个
            this.activeKey=[this.paddleData[0].id]
            // 通过险情ID获取全部任务地址信息
            this.getTaskAddsByEmergencyId(this.paddleData[0].id)
          }
        })
      },
      //加载
      getTaskAddsByEmergencyId(eId){
        let apiUrl = dispatchManage.getTaskAddsByEmergencyId
        let postList = [eId]
        postAction(apiUrl,postList).then((res)=>{
          if (res.success){
            console.log(res.result)
          }
        })
      },
      // 折叠板点击
      paddleChange(eId){
        console.log(eId)
        if (eId!==undefined) this.getTaskAddsByEmergencyId(eId)
      },
      // 折叠板设置icon
      handleClickSetting(event) {
        // If you don't want click extra trigger collapse, you can prevent this:
        event.stopPropagation();
      },
      //任务地址更改 button
      handleTaskEdit(record){
        this.clickMapPoint=!this.clickMapPoint
        this.clickTaskChangeId=record.key
      },
      //险情地址更改按钮
      emergencyAddressChange(item){
        console.log(item)
      },
      //任务地址显示 button
      handleTaskAddressShow(record){
        this.showMakerByAddress(record)
      },
      // 地点确认按钮
      lngLatConfirm(){
        data[this.clickTaskChangeId].taskAddress=this.address
        data[this.clickTaskChangeId].lngLat=this.lngLat
        this.$message.success('任务地点更改成功!')
        this.clickMapPoint=!this.clickMapPoint
      },
      // 初始化地图
      initMap(AMap) {
        let that = this
        that.map = new AMap.Map("map-container",{
          zoom:11,
        });
        that.map.on('click',function(e){
          if (that.clickMapPoint)reGeoCode(e.lnglat)
        })
        that.marker = new AMap.Marker();
        function reGeoCode(e) {
          that.map.add(that.marker);
          that.marker.setPosition([e.R,e.Q])
          AMap.plugin('AMap.Geocoder', function() {
            let geocoder = new AMap.Geocoder({
              city: '贵阳'
            })
            let lnglat = [e.R, e.Q]
            geocoder.getAddress(lnglat, function(status, result) {
              if (status === 'complete' && result.info === 'OK') {
                // result为对应的地理位置详细信息
                that.lngLat = String(e);
                that.address = result.regeocode.formattedAddress.substring(6);
              }
            })
          })
        }
      },
      // 地图移动到点击的地址
      showMakerByAddress(task){
        let that = this
        // 如果没有经纬度 根据地址来查询 且定位
        let lngLat
        if (task.lngLat === ''){
          AMap.plugin('AMap.Geocoder', function() {
            const geocoder = new AMap.Geocoder({
              // city 指定进行编码查询的城市，支持传入城市名、adcode 和 citycode
              city: '贵阳'
            })
            geocoder.getLocation(task.taskAddress, function(status, result) {
              if (status === 'complete' && result.info === 'OK') {
                let location = result.geocodes[0].location
                lngLat = [location.R, location.Q]
                setMakerAndMove(lngLat)
              }
            })
          })
        }else{
          lngLat = [task.lngLat.split(',')[0],task.lngLat.split(',')[1]]
          setMakerAndMove(lngLat)
        }
        function setMakerAndMove(lngLat) {
          that.map.add(that.marker);
          that.marker.setPosition(lngLat)
          that.map.setZoomAndCenter(15,lngLat)
          that.lngLat = String(lngLat)
          that.address=task.taskAddress
        }
      }
    }
  }
</script>

<style scoped>
  #map-container{
    padding:0;
    margin: 0;
    width: 100%;
    height: 600px;
  }
</style>