<?php
ini_set("memory_limit", "1024M");
require dirname(__FILE__).'/../core/init.php';

/* Do NOT delete this comment */
/* 不要删除这段注释 */

$configs = array(
    'name' => '新农网',
    'tasknum' => 10,
    'max_depth' => 1,
    'domains' => array(
        'www.xinnong.net',
        'xinnong.net',
    ),
    'scan_urls' => array(
        'http://www.xinnong.net/news/difang/ah/'
    ),
    'content_url_regexes' => array(
        "http://www.xinnong.net/news/\d+/\d+.html"
    ),
    'list_url_regexes' => array(
        "http://www.xinnong.net/news/difang/ah/list_1911_\d+.html"
    ),
    'export' => array(
        'type'  => 'sql',
        'file'  => PATH_DATA.'/gxgj.sql',
        'table' => 'gx',
    ),
    'fields' => array(
        array(
            // 抽取内容页的文章内容
            'name' => "title",
            'selector' => '//*[@class="arctit"]/h1',
            'required' => true
        ),
        array(
            // 抽取内容页的文章内容
            'name' => "time",
            'selector' => '//*[@class="arcinfo"]',
            'required' => true
        ),
        array(
            // 抽取内容页的文章内容
            'name' => "jianjie",
            'selector' => '//*[@class="arcdes"]',
            'required' => true
        ),
    ),
);
$start_time=microtime(true); //获取程序开始执行的时间

$spider = new phpspider($configs);
$spider->on_start = function ($spider) 
{
    // 生成列表页URL入队列
    for ($i = 1; $i <= 100; $i++) 
    {
        $url = 'http://www.xinnong.net/news/difang/ah/list_1911_'.$i.'.html';
        $spider->add_url($url);
    }
};
$spider->start();
$end_time=microtime(true);//获取程序执行结束的时间
$total=$end_time-$start_time; //计算差值
echo "RunTime:{$total}";