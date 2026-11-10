from pathlib import Path
import sys
p = Path(sys.argv[1])/'app/src/main/java/com/vasmarfas/UniversalAmbientLight/ui/studio/StudioScreen.kt'
s = p.read_text()
def swap(a,b):
 global s
 assert s.count(a)==1, f'patch mismatch: {a[:70]} ({s.count(a)})'
 s=s.replace(a,b,1)
swap('import androidx.compose.material3.Button\n', 'import androidx.compose.material3.Button\nimport androidx.compose.material3.AlertDialog\nimport androidx.compose.material3.MaterialTheme\nimport androidx.compose.material3.darkColorScheme\nimport androidx.compose.material3.OutlinedTextFieldDefaults\n')
swap('import androidx.compose.runtime.remember\n','import androidx.compose.runtime.remember\nimport androidx.compose.runtime.rememberCoroutineScope\n')
swap('import androidx.compose.ui.Alignment\n','import androidx.compose.ui.Alignment\nimport androidx.compose.ui.focus.onFocusChanged\n')
swap('import androidx.compose.ui.unit.sp\n','import androidx.compose.ui.unit.sp\nimport kotlinx.coroutines.launch\n')
swap('    val selected = config.segments.firstOrNull { it.id == selectedId }','    val selected = config.segments.firstOrNull { it.id == selectedId }\n    val leftScroll = rememberScrollState()\n    val rightScroll = rememberScrollState()\n    val scope = rememberCoroutineScope()')
swap('    Scaffold(\n        containerColor = ink,','''    MaterialTheme(colorScheme = darkColorScheme(
        primary = Color(0xFF286D74), onPrimary = snow,
        secondary = neon, onSecondary = ink,
        background = ink, onBackground = snow,
        surface = panel, onSurface = snow,
        surfaceVariant = Color(0xFF24334C), onSurfaceVariant = snow,
        outline = subtle
    )) {
    Scaffold(
        containerColor = ink,''')
swap('''                actions = {
                    Text(if (enabled) "● CUSTOM MAPPING ON" else "● ORIGINAL CAPTURE SAFE",''','''                actions = {
                    TextButton(onClick={scope.launch { leftScroll.animateScrollTo((leftScroll.value-500).coerceAtLeast(0)) }}) { Text("LEFT ▲", color=snow) }
                    TextButton(onClick={scope.launch { leftScroll.animateScrollTo((leftScroll.value+500).coerceAtMost(leftScroll.maxValue)) }}) { Text("LEFT ▼", color=snow) }
                    TextButton(onClick={scope.launch { rightScroll.animateScrollTo((rightScroll.value-500).coerceAtLeast(0)) }}) { Text("RIGHT ▲", color=snow) }
                    TextButton(onClick={scope.launch { rightScroll.animateScrollTo((rightScroll.value+500).coerceAtMost(rightScroll.maxValue)) }}) { Text("RIGHT ▼", color=snow) }
                    Text(if (enabled) "● CUSTOM MAPPING ON" else "● ORIGINAL CAPTURE SAFE",''')
swap('''                        OutlinedTextField(value = presetName, onValueChange = { presetName = it.take(48) },
                            singleLine = true, label = { Text("Name this scene") }, modifier = Modifier.fillMaxWidth())''','''                        TvEditField("Name this scene", presetName, { presetName=it.take(48) }, Modifier.fillMaxWidth(), maxLength=48)''')
swap('''                            OutlinedTextField(value = selected.name,
                                onValueChange = { edit(selected.copy(name = it.take(40))) },
                                singleLine = true, label = { Text("Zone name") }, modifier = Modifier.fillMaxWidth())''','''                            TvEditField("Zone name", selected.name, { edit(selected.copy(name=it.take(40))) }, Modifier.fillMaxWidth(), maxLength=40)''')
swap('.verticalScroll(rememberScrollState())) { main() }', '.verticalScroll(leftScroll)) { main() }')
swap('.verticalScroll(rememberScrollState())) { detail() }', '.verticalScroll(rightScroll)) { detail() }')
swap('.verticalScroll(rememberScrollState())) { main(); detail() }', '.verticalScroll(leftScroll)) { main(); detail() }')
swap('''        }
    }
}

@Composable
private fun StudioPanel''','''        }
    }
    }
}

@Composable
private fun StudioPanel''')
a=s.index('@Composable\nprivate fun NumericField(')
b=s.index('@Composable\nprivate fun Choice(',a)
s=s[:a]+'''// D-pad focus never opens the Fire TV IME. Only Select opens this explicit editor.
@Composable
private fun TvEditField(title:String, value:String, onChange:(String)->Unit,
                        modifier:Modifier=Modifier, keyboardType:KeyboardType=KeyboardType.Text,
                        maxLength:Int=64, valid:(String)->Boolean={true}) {
    var editing by remember { mutableStateOf(false) }
    var draft by remember(value, editing) { mutableStateOf(value) }
    var focused by remember { mutableStateOf(false) }
    OutlinedButton(onClick={draft=value; editing=true},
        modifier=modifier.onFocusChanged { focused=it.isFocused },
        border=BorderStroke(if(focused) 3.dp else 1.dp, if(focused) neon else subtle),
        colors=ButtonDefaults.outlinedButtonColors(contentColor=snow),
        shape=RoundedCornerShape(9.dp)) {
        Column(Modifier.fillMaxWidth()) {
            Text(title, color=if(focused) neon else subtle, fontSize=11.sp, maxLines=1)
            Text(value.ifBlank { "Select to enter" }, color=snow, fontSize=16.sp,
                maxLines=1, overflow=TextOverflow.Ellipsis)
        }
    }
    if(editing) AlertDialog(onDismissRequest={editing=false}, containerColor=panel,
        title={Text("Edit $title", color=snow)},
        text={Column(verticalArrangement=Arrangement.spacedBy(8.dp)) {
            Caption("Select the field to type. Choose Apply to save.")
            OutlinedTextField(value=draft, onValueChange={if(it.length<=maxLength) draft=it},
                singleLine=true, label={Text(title)},
                keyboardOptions=KeyboardOptions(keyboardType=keyboardType),
                colors=OutlinedTextFieldDefaults.colors(
                    focusedTextColor=snow, unfocusedTextColor=snow,
                    focusedContainerColor=Color(0xFF24334C),
                    unfocusedContainerColor=Color(0xFF24334C),
                    focusedBorderColor=neon, unfocusedBorderColor=subtle,
                    focusedLabelColor=neon, unfocusedLabelColor=subtle, cursorColor=neon))
            if(!valid(draft)) Text("Enter a valid value",color=Color(0xFFFFBC77))
        }},
        confirmButton={TextButton(enabled=valid(draft),onClick={onChange(draft);editing=false}) {
            Text("Apply",color=if(valid(draft)) neon else subtle)
        }},
        dismissButton={TextButton(onClick={editing=false}) { Text("Cancel",color=snow) }})
}
@Composable
private fun NumericField(title:String,value:String,onChange:(String)->Unit,modifier:Modifier=Modifier) {
    TvEditField(title,value,onChange,modifier,KeyboardType.Number,5,
        valid={it.toIntOrNull()?.let { n->n in 1..2048 }==true})
}
@Composable
private fun NumberSetting(title:String,value:Int,range:IntRange,modifier:Modifier=Modifier,
                          onChange:(Int)->Unit) {
    TvEditField(title,value.toString(),{it.toIntOrNull()?.takeIf { n->n in range }?.let(onChange)},
        modifier,KeyboardType.Number,5,valid={it.toIntOrNull()?.let { n->n in range }==true})
}
@Composable
private fun HexColorSetting(title:String,color:Int,modifier:Modifier=Modifier,onChange:(Int)->Unit) {
    TvEditField(title,"%06X".format(color and 0xFFFFFF),
        {it.toIntOrNull(16)?.let(onChange)},modifier,KeyboardType.Text,6,
        valid={it.length==6 && it.all { c->c.isDigit() || c.uppercaseChar() in 'A'..'F' }})
}

'''+s[b:]
p.write_text(s)
print('LivingLighting Fire TV remote patch applied')
