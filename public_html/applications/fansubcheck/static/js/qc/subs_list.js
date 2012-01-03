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
    'Ext.ux.SlidingPager',
    'Ext.ux.form.MultiSelect',
    'Ext.ux.form.ItemSelector'
]);

function renderIcon(val) {
    return '<img src="' + val + '" height="30">';
}

function formatDate(value){
    return value ? Ext.Date.dateFormat(value, 'M d, Y') : '';
}

function get(name){
   if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
      return decodeURIComponent(name[1]);
}

Ext.application({
    name: 'HelloExt',
    launch: function() {
	
		Ext.state.Manager.setProvider(Ext.create('Ext.state.CookieProvider'));
	
        // Set up a model to use in our Store
		Ext.define('Sub', {
			extend: 'Ext.data.Model',
			fields: [
                {name: 'id', type: 'int'},
				{name: 'start_time', type: 'string'},
				{name: 'text', type: 'string'},
				{name: 'comments_nb', type: 'int'},
				{name: 'episode', type: 'int'},
				{name: 'lastcomment_date', type: 'date'}
			]
		});

        var a=location.pathname.split('/');

		var myStore = Ext.create('Ext.data.Store', {
			model: 'Sub',
            pageSize: 20,
            remoteSort: true,
            remoteFilter: false,
			proxy: {
				type: 'ajax',
				url : '/fansubcheck/default/subs_list.json/'+a[a.length-2]+'/'+a[a.length-1],
				reader: {
					type: 'json',
					root: 'subs'
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
				type: 'string',
				dataIndex: 'start_time',
				disabled: false
			}, {
				type: 'string',
				dataIndex: 'text',
				disabled: false
			}, {
				type: 'numeric',
				dataIndex: 'comments_nb',
				disabled: false
			}, {
				type: 'date',
				dataIndex: 'lastcomment_date',
				disabled: false
			}]
		};
		
		Ext.fly('subs_list').update('');

		var grid = Ext.create('Ext.grid.Panel', {
			//renderTo: Ext.getBody(),
			renderTo: "subs_list",
            id: 'subsGrid',
			store: myStore,
			stateful: true,
			stateId: 'stateSubs',
            remoteSort: true,
            remoteFilter: false,
			width: "100%",
			autoHeight: true,
			title: 'Sous-titres',
			features: [filters],
			columns: [
				{
					text: 'Time',
					width: 75,
					dataIndex: 'start_time',
					sortable: true,
					hideable: false,
					filterable: true
				},
                {
					text: 'Texte',
					flex: 1,
					sortable: true,
					hideable: false,
					dataIndex: 'text',
					filterable: true
				},
                {
					text: 'Commentaires',
					width: 50,
                    align: 'center',
					sortable: true,
					hideable: false,
					dataIndex: 'comments_nb',
					filterable: true
				},
                {
					text: 'Dernier',
					width: 90,
                    align: 'center',
					sortable: true,
					hideable: false,
					dataIndex: 'lastcomment_date',
                    renderer: formatDate,
					filterable: true
				}
			],
            bbar: Ext.create('Ext.PagingToolbar', {
                pageSize: 20,
                store: myStore,
                displayInfo: true,
                plugins: Ext.create('Ext.ux.SlidingPager', {})
            }),
            tbar: Ext.create('Ext.PagingToolbar', {
                pageSize: 20,
                store: myStore,
                displayInfo: true,
                plugins: Ext.create('Ext.ux.SlidingPager', {})
            })
		});
		grid.filters;
        // set up onclick event for each row
        grid.addListener("cellclick", function(iView, iCellEl, iColIdx, iStore, iRowEl, iRowIdx, iEvent) {
            var zRec = iView.getRecord(iRowEl);
            // create a grid and display the comments for that sub
            // Set up a model to use in our Store
            Ext.define('Comment', {
                extend: 'Ext.data.Model',
                fields: [
                    {name: 'created_on', type: 'date', mapping: 'comment.created_on'},
                    {name: 'content', type:'html', mapping: 'comment.content'},
                    {name: 'author', type: 'string', mapping: 'auth_user.username'}
                ]
            });

            var subId= zRec.data.id;
            var episodeId= zRec.data.episode;

            var commentsStore = Ext.create('Ext.data.Store', {
                model: 'Comment',
                proxy: {
                    type: 'ajax',
                    url : '/fansubcheck/default/get_comments.json/'+subId,
                    reader: {
                        type: 'json',
                        root: 'comments'
                    }
                },
                autoLoad: true
            });

            Ext.fly('comments_list').update('');

            var commentsGrid = Ext.create('Ext.grid.Panel', {
                //renderTo: Ext.getBody(),
                renderTo: "comments_list",
                id: 'commentsGrid',
                store: commentsStore,
                stateful: true,
                stateId: 'stateComments',
                width: "100%",
                autoHeight: true,
                title: 'Commentaires du sous-titre: '+zRec.data.text,
                columns: [
                    {
                        text: 'Date',
                        width: 90,
                        dataIndex: 'created_on',
                        sortable: false,
                        hideable: false
                        ,renderer: formatDate
                    },
                    {
                        text: 'Auteur',
                        width: 100,
                        sortable: false,
                        hideable: false,
                        dataIndex: 'author'
                    },
                    {
                        text: 'Contenu',
                        flex: 1,
                        sortable: false,
                        hideable: false,
                        //renderer: Ext.util.Format.htmlDecode,
                        dataIndex: 'content'
                    }
                ],
                bbar    : [
                  {
                    text    : 'Reload',
                    handler : function() {
                        //refresh source grid
                        commentsStore.load();
                        myStore.load();
                    }
                  }
                ]
            });

            Ext.fly('add_comment_form').update('');

            // Add a form to add a comment
            var top = Ext.create('Ext.form.Panel', {
                frame:false,
                //title: 'Add a comment',
                bodyStyle:'padding:5px 5px 0',
                width: '90%',
                url: '/fansubcheck/default/call_qc/json/post_comment/',
                renderTo: "add_comment_form",
                fieldDefaults: {
                    labelAlign: 'top',
                    msgTarget: 'side'
                },

                items: [{
                    xtype: 'htmleditor',
                    name: 'comment_content',
                    fieldLabel: 'Ajouter un commentaire',
                    height: 150,
                    anchor: '100%'
                }, {
                    xtype: 'hiddenfield',
                    name: 'sub_id',
                    value: subId
                }, {
                    xtype: 'hiddenfield',
                    name: 'episode_id',
                    value: episodeId
                }],

                buttons: [{
                    text: 'Poster',
                    handler: function() {
                        // The getForm() method returns the Ext.form.Basic instance:
                        var form = this.up('form').getForm();
                        if (form.isValid()) {
                            // Submit the Ajax request and handle the response
                            form.submit({
                                success: function(form, action) {
                                    Ext.fly('add_comment_form').update('Comment added!');
                                    commentsStore.load();
                                    myStore.load();
                                },
                                failure: function(form, action) {
                                    Ext.Msg.alert('Failed', action.result.msg);
                                }
                            });
                        }
                    }
                }]
            });

            document.getElementById('comments_list').focus();


        });

    }
});