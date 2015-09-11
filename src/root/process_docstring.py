with open('nested.html') as docstrings:
    




<table class="docutils field-list" frame="void" rules="none">
<col class="field-name" />
<col class="field-body" />
<tbody valign="top">
<tr class="field-odd field"><th class="field-name">Parameters:</th><td class="field-body"><p class="first"><strong>in_streams</strong> : list of streams</p>
<p><strong>out_streams</strong> : list of streams</p>
<p><strong>call_streams</strong> : list of streams</p>
<blockquote>
<div><p>When a new value is added to a stream in this list
a state transition is invoked.
This the usual way (but not the only way) in which
state transitions occur.</p>
</div></blockquote>
<p><strong>state: object</strong></p>
<blockquote>
<div><p>The state of the agent. The state is updated after
a transition.</p>
</div></blockquote>
<p><strong>transition: function</strong></p>
<blockquote>
<div><p>This function is called by next() which
is the state-transition operation for this agent.
An agent&#8217;s state transition is specified by
its transition function.</p>
</div></blockquote>
<p><strong>stream_manager</strong> : function</p>
<blockquote>
<div><p>Each stream has management variables, such as whether
the stream is open or closed. After a state-transition
the agent executes the stream_manager function
to modify the management variables of the agent&#8217;s output
and call streams.</p>
</div></blockquote>
<p><strong>name</strong> : str, optional</p>
<blockquote class="last">
<div><p>name of this agent</p>
</div></blockquote>
</td>
</tr>
</tbody>
</table>