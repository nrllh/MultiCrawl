# BigQuery Table Schema

## requests
id:INTEGER, browser_id:STRING, site_id:INTEGER, subpage_id:INTEGER, visit_id:STRING, url:STRING, top_level_url:STRING, method:STRING, referrer:STRING, headers:STRING, is_XHR:INTEGER, is_third_party_channel:INTEGER, is_third_party_to_top_window:INTEGER, resource_type:STRING, time_stamp:DATETIME, is_websocket:INTEGER, body:STRING, etld:STRING, content_hash:STRING, is_tracker:INTEGER, is_background_req:INTEGER, in_scope:INTEGER, window_id:INTEGER, tab_id:INTEGER, frame_id:INTEGER, parent_frame_id:INTEGER, frame_ancestors:STRING, request_id:INTEGER, triggering_origin:STRING, loading_origin:STRING, loading_href:STRING, req_call_stack:STRING, post_body:STRING, post_body_raw:STRING

## responses
id:INTEGER,browser_id:STRING,site_id:INTEGER,subpage_id:INTEGER,visit_id:STRING,url:STRING,time_stamp:DATETIME,response_status:STRING,response_status_text:STRING,content_hash:STRING,headers:STRING,body:STRING,etld:STRING,method:STRING,is_background_response:INTEGER,is_tracker:INTEGER,resource_type:STRING,in_scope:INTEGER, 


## cookies
id:STRING, browser_id:STRING, site_id:INTEGER, visit_id:STRING, expiry:DATETIME, is_secure:INTEGER, is_http_only:INTEGER, same_site:STRING, name:STRING, value:STRING, host:STRING, path:STRING, time_stamp:DATETIME, is_host_only:INTEGER, is_session:INTEGER, is_third_party:INTEGER, is_session_common:INTEGER, in_scope:INTEGER, subpage_id:INTEGER,

## localstorage
browser_id:STRING,site_id:BYTES,origin_attributes:STRING,origin_key:STRING,scope:STRING,key:STRING,value:STRING,in_scope:INTEGER

## callstacks
visit_id:STRING,site_id:STRING,subpage_id:STRING,browser_id:STRING,request_id:STRING,call_stack:STRING

## dns_responses
id:INTEGER,site_id:STRING,subpage_id:STRING,visit_id:STRING,browser_id:STRING,request_id:STRING,hostname:STRING,addresses:STRING,used_address:STRING,canonical_name:STRING,is_TRR:INTEGER,time_stamp:DATETIME

## javascript
id:INTEGER, site_id:STRING, subpage_id:STRING, visit_id:STRING, browser_id:STRING, request_id:STRING, incognito:STRING, event_ordinal:STRING, page_scoped_event_ordinal:STRING, window_id:STRING, tab_id:STRING, frame_id:STRING, script_url:STRING, script_line:STRING, script_col:STRING, func_name:STRING, script_loc_eval:STRING, document_url:STRING, top_level_url:STRING, call_stack:STRING, symbol:STRING, operation:STRING, value:STRING, arguments:STRING

## http_redirects
id:INTEGER,site_id:STRING,subpage_id:STRING,visit_id:STRING,browser_id:STRING,request_id:STRING,incognito:STRING,old_request_url:STRING,old_request_id:STRING,new_request_url:STRING,window_id:STRING,tab_id:STRING,frame_id:STRING,response_status:STRING,response_status_text:STRING,headers:STRING,time_stamp:STRING

## incomplete_visits
id:INTEGER,site_id:STRING,subpage_id:STRING,visit_id:STRING,browser_id:STRING,request_id:STRING

## navigations
id:INTEGER,site_id:STRING,subpage_id:STRING,visit_id:STRING,browser_id:STRING,request_id:STRING,incognito:STRING,extension_session_uuid:STRING,process_id:STRING,window_id:STRING,tab_id:STRING,tab_opener_tab_id:STRING,frame_id:STRING,parent_frame_id:STRING,window_width:STRING,window_height:STRING,window_type:STRING,tab_width:STRING,tab_height:STRING,tab_cookie_store_id:STRING,uuid:STRING,url:STRING,transition_qualifiers:STRING,transition_type:STRING,before_navigate_event_ordinal:STRING,before_navigate_time_stamp:STRING,committed_event_ordinal:STRING,committed_time_stamp:STRING

# tree_page_level

site_id:INTEGER,subpage_id:INTEGER,visit_id:STRING,browser_id:STRING,first_nodes:STRING,openwpm_interaction_1:STRING,openwpm_interaction_2:STRING,openwpm_interaction_old:STRING,openwpmheadless_interaction:STRING,openwpm_desktop:STRING

# accept_all_logs

id:INTEGER, browser_id:STRING, visit_id:STRING, site_id:INTEGER, log:STRING