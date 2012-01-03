Ext.Loader.setConfig({enabled: true});
Ext.Loader.setPath('Ext.ux', '/fansubcheck/static/js/ext/examples/ux');
Ext.require([
    'Ext.grid.*',
    'Ext.data.*',
    'Ext.util.*',
    'Ext.state.*',
	'Ext.ux.grid.FiltersFeature',
    'Ext.toolbar.Paging',
    'Ext.ux.data.PagingMemoryProxy',
    'Ext.ux.SlidingPager'
]);

function renderIcon(val) {
    return '<img src="' + val + '" height="30">';
}

function get(name){
   if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
      return decodeURIComponent(name[1]);
   else
      return "0";
}

function isPublic() {
    var a=location.pathname.split('/');
    if (a[a.length-1]=="public_qc_list")
        return true;
    return false;
}

function formatDate(value){
    return value ? Ext.Date.dateFormat(value, 'M d, Y') : '';
}

Ext.application({
    name: 'HelloExt',
    launch: function() {
	
		Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));
	
        // Set up a model to use in our Store
		Ext.define('QC', {
			extend: 'Ext.data.Model',
			fields: [
				{name: 'id', type: 'int'},
				{name: 'name', type: 'string'},
				{name: 'subs_nb', type: 'int'},
				{name: 'created_on', type: 'date'},
                {name: 'comments_nb', type: 'int'},
                {name: 'lastcomment_date', type: 'date'},
                {name: 'is_public', type: 'bool'},
                {name: 'allow_qcteam', type: 'bool'},
                {name: 'key', type: 'string'}
			]
		});

        var qcListTitle= 'Mes QC';
        var qcListURL = '/fansubcheck/default/my_qc_list.json';
        if (isPublic()) {
            qcListTitle="Public QC";
            qcListURL = '/fansubcheck/default/get_public_qc_list.json';
        }

		var myStore = Ext.create('Ext.data.Store', {
			model: 'QC',
            pageSize: 10,
            remoteSort: true,
            remoteFilter: false,
			proxy: {
				type: 'ajax',
				url : qcListURL,
				reader: {
					type: 'json',
					root: 'episodes'
				}
			},
			autoLoad: true
		});
	    var filters = {
			ftype: 'filters',
			// encode and local configuration options defined previously for easier reuse
			encode: true, // json encode the filter query
			local: true,   // defaults to false (remote filtering)
			filters: [{
				type: 'numeric',
				dataIndex: 'subs_nb'
			}, {
				type: 'string',
				dataIndex: 'name',
				disabled: false
			}, {
				type: 'date',
				dataIndex: 'created_on',
                renderer: formatDate,
				disabled: false
			}, {
				type: 'numeric',
				dataIndex: 'comments_nb',
				disabled: false
			}, {
				type: 'date',
				dataIndex: 'lastcomment_date',
				disabled: false
			}, {
				type: 'boolean',
				dataIndex: 'is_public',
				disabled: false
			}, {
				type: 'boolean',
				dataIndex: 'allow_qcteam',
				disabled: false
			}]
		};
		
		Ext.fly('qc_list').update('');

		var grid = Ext.create('Ext.grid.Panel', {
			//renderTo: Ext.getBody(),
			renderTo: "qc_list",
			store: myStore,
			stateful: true,
			stateId: 'stateQCList',
            remoteSort: true,
            remoteFilter: false,
			width: "100%",
			autoHeight: true,
			title: qcListTitle,
			features: [filters],
			columns: [
				{
					text: 'Nom',
					flex: 1,
					dataIndex: 'name',
					sortable: true,
					hideable: false,
					filterable: true
				},
                {
					text: 'Lignes',
					width: 50,
					sortable: true,
					hideable: true,
					dataIndex: 'subs_nb',
					filterable: true
				},
                {
					text: 'Date',
					width: 90,
					sortable: true,
					hideable: true,
					dataIndex: 'created_on',
                    renderer: formatDate,
					filterable: true
				},
                {
					text: 'Commentaires',
					width: 60,
					sortable: true,
					hideable: true,
					dataIndex: 'comments_nb',
					filterable: true
				},
                {
					text: 'Dernier Commentaire',
					width: 90,
					sortable: true,
					hideable: true,
					dataIndex: 'lastcomment_date',
                    renderer: formatDate,
					filterable: true
				},
                {
					text: 'Public',
					width: 50,
					sortable: true,
					hideable: true,
					dataIndex: 'is_public',
					filterable: true
				},
                {
					text: 'QC Team',
					width: 50,
					sortable: true,
					hideable: true,
					dataIndex: 'allow_qcteam',
					filterable: true
				}
			],
            bbar: Ext.create('Ext.PagingToolbar', {
                pageSize: 10,
                store: myStore,
                displayInfo: true,
                plugins: Ext.create('Ext.ux.SlidingPager', {})
            }),
            tbar: Ext.create('Ext.PagingToolbar', {
                pageSize: 10,
                store: myStore,
                displayInfo: true,
                plugins: Ext.create('Ext.ux.SlidingPager', {})
            })
		});
		grid.filters;
        // set up onclick event for each row
        grid.addListener("cellclick", function(iView, iCellEl, iColIdx, iStore, iRowEl, iRowIdx, iEvent) {
		        var zRec = iView.getRecord(iRowEl);
		        //alert(zRec.data.name);
		        //window.open('/default/show_qc/' + zRec.data.key);
                location.href= '/fansubcheck/default/show_qc/' + zRec.data.id + '/' + zRec.data.key
            });

    }
});