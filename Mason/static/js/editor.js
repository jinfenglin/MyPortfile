/**
 * Created by jinfenglin on 7/18/16.
 */
$(function turnAffixClickOff(){
    $( '.tool-belt' ).on( 'affix.bs.affix', function(){
    if( !$( window ).scrollTop() ) return false;
} );
})