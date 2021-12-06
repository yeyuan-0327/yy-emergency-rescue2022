package org.jeecg.modules.demo.datamanage.controller;

import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;
import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import org.jeecg.common.api.vo.Result;
import org.jeecg.common.system.query.QueryGenerator;
import org.jeecg.common.util.oConvertUtils;
import org.jeecg.modules.demo.datamanage.entity.DatabaseInfo;
import org.jeecg.modules.demo.datamanage.service.IDatabaseInfoService;

import com.baomidou.mybatisplus.core.conditions.query.QueryWrapper;
import com.baomidou.mybatisplus.core.metadata.IPage;
import com.baomidou.mybatisplus.extension.plugins.pagination.Page;
import lombok.extern.slf4j.Slf4j;

import org.jeecgframework.poi.excel.ExcelImportUtil;
import org.jeecgframework.poi.excel.def.NormalExcelConstants;
import org.jeecgframework.poi.excel.entity.ExportParams;
import org.jeecgframework.poi.excel.entity.ImportParams;
import org.jeecgframework.poi.excel.view.JeecgEntityExcelView;
import org.jeecg.common.system.base.controller.JeecgController;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.multipart.MultipartHttpServletRequest;
import org.springframework.web.servlet.ModelAndView;
import com.alibaba.fastjson.JSON;
import io.swagger.annotations.Api;
import io.swagger.annotations.ApiOperation;
import org.jeecg.common.aspect.annotation.AutoLog;

 /**
 * @Description: 基础数据库信息表
 * @Author: jeecg-boot
 * @Date:   2021-08-01
 * @Version: V1.0
 */
@Api(tags="基础数据库信息表")
@RestController
@RequestMapping("/datamanage/databaseInfo")
@Slf4j
public class DatabaseInfoController extends JeecgController<DatabaseInfo, IDatabaseInfoService> {
	@Autowired
	private IDatabaseInfoService databaseInfoService;

	/**
	 * 分页列表查询
	 *
	 * @param databaseInfo
	 * @param pageNo
	 * @param pageSize
	 * @param req
	 * @return
	 */
	@AutoLog(value = "基础数据库信息表-分页列表查询")
	@ApiOperation(value="基础数据库信息表-分页列表查询", notes="基础数据库信息表-分页列表查询")
	@GetMapping(value = "/list")
	public Result<?> queryPageList(DatabaseInfo databaseInfo,
								   @RequestParam(name="pageNo", defaultValue="1") Integer pageNo,
								   @RequestParam(name="pageSize", defaultValue="10") Integer pageSize,
								   HttpServletRequest req) {
		QueryWrapper<DatabaseInfo> queryWrapper = QueryGenerator.initQueryWrapper(databaseInfo, req.getParameterMap());
		Page<DatabaseInfo> page = new Page<DatabaseInfo>(pageNo, pageSize);
		IPage<DatabaseInfo> pageList = databaseInfoService.page(page, queryWrapper);
		return Result.OK(pageList);
	}
	
	/**
	 *   添加
	 *
	 * @param databaseInfo
	 * @return
	 */
	@AutoLog(value = "基础数据库信息表-添加")
	@ApiOperation(value="基础数据库信息表-添加", notes="基础数据库信息表-添加")
	@PostMapping(value = "/add")
	public Result<?> add(@RequestBody DatabaseInfo databaseInfo) {
		databaseInfoService.save(databaseInfo);
		return Result.OK("添加成功！");
	}
	
	/**
	 *  编辑
	 *
	 * @param databaseInfo
	 * @return
	 */
	@AutoLog(value = "基础数据库信息表-编辑")
	@ApiOperation(value="基础数据库信息表-编辑", notes="基础数据库信息表-编辑")
	@PutMapping(value = "/edit")
	public Result<?> edit(@RequestBody DatabaseInfo databaseInfo) {
		databaseInfoService.updateById(databaseInfo);
		return Result.OK("编辑成功!");
	}
	
	/**
	 *   通过id删除
	 *
	 * @param id
	 * @return
	 */
	@AutoLog(value = "基础数据库信息表-通过id删除")
	@ApiOperation(value="基础数据库信息表-通过id删除", notes="基础数据库信息表-通过id删除")
	@DeleteMapping(value = "/delete")
	public Result<?> delete(@RequestParam(name="id",required=true) String id) {
		databaseInfoService.removeById(id);
		return Result.OK("删除成功!");
	}
	
	/**
	 *  批量删除
	 *
	 * @param ids
	 * @return
	 */
	@AutoLog(value = "基础数据库信息表-批量删除")
	@ApiOperation(value="基础数据库信息表-批量删除", notes="基础数据库信息表-批量删除")
	@DeleteMapping(value = "/deleteBatch")
	public Result<?> deleteBatch(@RequestParam(name="ids",required=true) String ids) {
		this.databaseInfoService.removeByIds(Arrays.asList(ids.split(",")));
		return Result.OK("批量删除成功!");
	}
	
	/**
	 * 通过id查询
	 *
	 * @param id
	 * @return
	 */
	@AutoLog(value = "基础数据库信息表-通过id查询")
	@ApiOperation(value="基础数据库信息表-通过id查询", notes="基础数据库信息表-通过id查询")
	@GetMapping(value = "/queryById")
	public Result<?> queryById(@RequestParam(name="id",required=true) String id) {
		DatabaseInfo databaseInfo = databaseInfoService.getById(id);
		if(databaseInfo==null) {
			return Result.error("未找到对应数据");
		}
		return Result.OK(databaseInfo);
	}

    /**
    * 导出excel
    *
    * @param request
    * @param databaseInfo
    */
    @RequestMapping(value = "/exportXls")
    public ModelAndView exportXls(HttpServletRequest request, DatabaseInfo databaseInfo) {
        return super.exportXls(request, databaseInfo, DatabaseInfo.class, "基础数据库信息表");
    }

    /**
      * 通过excel导入数据
    *
    * @param request
    * @param response
    * @return
    */
    @RequestMapping(value = "/importExcel", method = RequestMethod.POST)
    public Result<?> importExcel(HttpServletRequest request, HttpServletResponse response) {
        return super.importExcel(request, response, DatabaseInfo.class);
    }
	// 下述为袁野人工编写
	@RequestMapping(value = "/clickDetailTable", method = RequestMethod.POST)
	 public Result<?> clickDetailTable(@RequestBody List<String> tableName){
    	List<Map<String,Object>> tableData = databaseInfoService.selectClickTableData(tableName);
    	return Result.OK(tableData);
	}

	 @RequestMapping(value = "/selectCharGroupByField", method = RequestMethod.POST)
	 public Result<?> selectCharGroupByField(@RequestBody List<String> fieldName){
		 List<Map<String,Object>> fieldData = databaseInfoService.selectCharGroupByField(fieldName);
		 return Result.OK(fieldData);
	 }

 }
